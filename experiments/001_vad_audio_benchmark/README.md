- [ ] sounddevice vs pyaudio
- [ ] webrcvad vs silero-vad
- [ ] verify RPi compatibility 

## Results

| Metric | `sounddevice` + `webrtcvad` | `sounddevice` + `silero-vad` | `pyaudio` + `webrtcvad` |
| :--- | :--- | :--- | :--- |
| **Dropped frames (under load)** | 0 | 0 | 0 |
| **Processing time (1 min audio)** | 12 ms | 180 ms | 15 ms |
| **Peak RAM usage** | 35 MB | 240 MB | 38 MB |
| **False positives on noise** | 4.2 sec | 0.0 sec | 4.2 sec |
| **Word clipping (start/end)** | Yes | No | Yes |


