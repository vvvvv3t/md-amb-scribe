from rapidfuzz import fuzz

def update_with_clean(self, seg_id: int, whisper_text: str):
    if seg_id not in self.segments:
        return
        
    vosk_text = self.segments[seg_id].text
    clean_text = whisper_text.strip()
    
    # Защита от пустоты или галлюцинаций Whisper
    if not clean_text:
        return
        
    # Если Whisper нафантазировал текст в 3 раза длиннее черновика Vosk
    if len(vosk_text) > 0 and len(clean_text) > len(vosk_text) * 2.5:
        self.segments[seg_id].low_confidence = True
        return # Оставляем более надежный черновик Vosk

    # Если тексты совсем не похожи друг на друга (меньше 35% совпадения)
    if vosk_text and fuzz.token_set_ratio(vosk_text, clean_text) < 35:
        self.segments[seg_id].low_confidence = True

    self.segments[seg_id].text = clean_text
    self.segments[seg_id].is_clean = True
