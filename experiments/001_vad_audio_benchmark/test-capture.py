import time
import numpy as np
import pyaudio
import sounddevice as sd

SAMPLE_RATE = 16000
CHUNK_SAMPLES = 512  # 32 ms
TEST_SECONDS = 15    # test latency

# stress
def stress_cpu():
    a = np.random.rand(300, 300)
    np.dot(a, a)


def test_sounddevice():
    overflows = 0
    convert_times = []
    total_chunks = int((SAMPLE_RATE / CHUNK_SAMPLES) * TEST_SECONDS)

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="float32", blocksize=CHUNK_SAMPLES) as stream:
        for _ in range(total_chunks):
            t0 = time.perf_counter()
            data, overflowed = stream.read(CHUNK_SAMPLES)
            # 
            _ = data.flatten()
            convert_times.append(time.perf_counter() - t0)

            if overflowed:
                overflows += 1
            stress_cpu()

    avg_ms = (sum(convert_times) / len(convert_times)) * 1000
    print(f"[sounddevice] Потерь кадров: {overflows} | Среднее время чтения: {avg_ms:.2f} мс")


def test_pyaudio():
    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK_SAMPLES,
    )

    overflows = 0
    convert_times = []
    total_chunks = int((SAMPLE_RATE / CHUNK_SAMPLES) * TEST_SECONDS)

    for _ in range(total_chunks):
        t0 = time.perf_counter()
        try:
            raw_bytes = stream.read(CHUNK_SAMPLES, exception_on_overflow=True)
            # pyaudio отдает сырые байты, нужно переводить в float32 для нейросети
            audio_int16 = np.frombuffer(raw_bytes, dtype=np.int16)
            _ = audio_int16.astype(np.float32) / 32768.0
        except IOError:
            overflows += 1
        convert_times.append(time.perf_counter() - t0)
        stress_cpu()

    stream.stop_stream()
    stream.close()
    pa.terminate()

    avg_ms = (sum(convert_times) / len(convert_times)) * 1000
    print(f"[pyaudio]     Потерь кадров: {overflows} | Среднее время чтения: {avg_ms:.2f} мс")


if __name__ == "__main__":
    print("Старт теста захвата звука (15 сек на каждую библиотеку)...\n")
    test_sounddevice()
    test_pyaudio()

