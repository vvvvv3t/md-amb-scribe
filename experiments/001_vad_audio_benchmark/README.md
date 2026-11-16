- [ ] sounddevice vs pyaudio
- [ ] webrcvad vs silero-vad
- [ ] verify RPi compatibility 

## Results

| Metric | `sounddevice` + `webrtcvad` | `sounddevice` + `silero-vad` | `pyaudio` + `webrtcvad` |
| :--- | :--- | :--- | :--- |
| **Dropped frames (under load)** | 0 | 0 | 0 |
| **Processing time (1 min audio)** | 0 ms | 0 ms | 0 ms |
| **Peak RAM usage** | 0 MB | 0 MB | 0 MB |
| **False positives on noise** | 0.0 sec | 0.0 sec | 0.0 sec |
| **Word clipping (start/end)** | - | - | - |


