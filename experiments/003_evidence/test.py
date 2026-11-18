import time
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Segment:
    id: int
    start: float
    end: float
    text: str
    is_clean: bool = False  # False = черновик Vosk, True = чистовик Whisper

class TranscriptBuffer:
    def __init__(self):
        self.segments: Dict[int, Segment] = {}
        self.next_id = 1

    # 1. Вызывается мгновенно из потока Vosk (Speed Layer)
    def add_draft(self, start: float, end: float, vosk_text: str) -> int:
        seg_id = self.next_id
        self.next_id += 1
        self.segments[seg_id] = Segment(
            id=seg_id,
            start=round(start, 2),
            end=round(end, 2),
            text=vosk_text,
            is_clean=False
        )
        return seg_id

    # 2. Вызывается из потока Whisper (Batch Layer) после обработки чанка VAD
    def update_with_clean(self, seg_id: int, whisper_text: str, words_timestamps: list = None):
        if seg_id in self.segments:
            # Перезаписываем черновик чистым текстом с пунктуацией
            self.segments[seg_id].text = whisper_text.strip()
            self.segments[seg_id].is_clean = True
            
            # Если Whisper вернул уточненные границы фразы, обновляем их
            if words_timestamps:
                self.segments[seg_id].start = round(words_timestamps[0]['start'], 2)
                self.segments[seg_id].end = round(words_timestamps[-1]['end'], 2)

    # 3. Формирует промпт для LLM с ID, чтобы она вернула evidence_ids
    def get_prompt_context(self) -> str:
        lines = []
        for seg in self.segments.values():
            lines.append(f"[ID:{seg.id}] {seg.text}")
        return "\n".join(lines)

    # 4. Пост-обработка ответа LLM: подставляем таймстампы и цитаты по ID
    def enrich_json_with_evidence(self, llm_json: dict) -> dict:
        for field_name, data in llm_json.items():
            if isinstance(data, dict) and "evidence_ids" in data:
                ev_list = []
                for eid in data["evidence_ids"]:
                    if eid in self.segments:
                        seg = self.segments[eid]
                        ev_list.append({
                            "id": seg.id,
                            "time": f"{seg.start}s - {seg.end}s",
                            "quote": seg.text
                        })
                data["evidence_details"] = ev_list
        return llm_json
