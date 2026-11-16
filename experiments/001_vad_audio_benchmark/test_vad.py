import time
import wave
import numpy as np
import psutil
import torch
import webrtcvad

wav_path = ; #clean.wav / noice / silence + clicks

def read_wav (path):
    with wave.open (path "rb") as wf,
assert wf.getnchannels() = 1
        assert getframerste()= 1600,
        assert getsampwidth () = 2
        raw_bytes = wf.readframes (wf.getnchannels())
        return raw_bytes


def save_wav(path, raw_bytes):
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(raw_bytes)
        
#webrtcvad test
        
def test_webrtcvad(raw_bytes, mode=3):
    vad = webrtcvad.Vad(mode)
    chunk_bytes = 960
    speech_chunks = []
    
start_time = time.perf_counter()
    for i in range(0, len(raw_bytes) - chunk_bytes, chunk_bytes):
        chunk = raw_bytes[i : i + chunk_bytes]
        if vad.is_speech(chunk, 16000):
            speech_chunks.append(chunk)
    elapsed = time.perf_counter() - start_time

    out_bytes = b"".join(speech_chunks)
    save_wav("out_webrtc.wav", out_bytes)
    return elapsed, len(out_bytes) / 32000  # time counter
    
# test silero

def test_silero(raw_bytes, threshold=0.5):
    model, _ = torch.hub.load(
        repo_or_dir="snakers4/silero-vad", model="silero_vad", trust_repo=True
    )
audio_int16 = np.frombuffer(raw_bytes, dtype=np.int16)
    audio_float32 = audio_int16.astype(np.float32) / 32768.0

    # 
    chunk_samples = 512
    speech_chunks = []
    
start_time = time.perf_counter()
    for i in range(0, len(audio_float32) - chunk_samples, chunk_samples):
        chunk = torch.from_numpy(audio_float32[i : i + chunk_samples])
        prob = model(chunk, 16000).item()
        if prob >= threshold:
            speech_chunks.append(audio_int16[i : i + chunk_samples].tobytes())
    elapsed = time.perf_counter() - start_time
    
     out_bytes = b"".join(speech_chunks)
    save_wav("out_silero.wav", out_bytes)
    return elapsed, len(out_bytes) / 32000


if __name__ == "__main__":
    process = psutil.Process()
    raw_audio = read_wav(WAV_PATH)
    total_sec = len(raw_audio) / 32000
    print(f"Длительность исходника: {total_sec:.2f} сек.\n")

    t_web, sec_web = test_webrtcvad(raw_audio)
    print(f"[WebRTC VAD] Обработано за {t_web*1000:.1f} мс | Найдено речи: {sec_web:.2f} сек.")

    t_sil, sec_sil = test_silero(raw_audio)
    ram_mb = process.memory_info().rss / (1024 * 1024)
    print(f"[Silero VAD] Обработано за {t_sil*1000:.1f} мс | Найдено речи: {sec_sil:.2f} сек.")
    print(f"Потребление RAM процесса: {ram_mb:.1f} МБ")