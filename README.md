# md-amb-scribe
offline medical documentation pipeline
## Goals

- offline
- no cloud
- low latency
- realtime
- algorithm-first
- local llm

## Roadmap

- [x] JSON extraction
- [ ] streaming
- [ ] VAD ?
- [ ] realtime pipeline
- [ ] stopword filtering
- [ ] noise reduction

- [ ] chunks + VAD
- [ ] 2 flows (lambda)
- [ ] timestops
- [ ] initial_prompt: + Doctor Onboarding Script (dict_json and examples.txt)
- [ ] defauit_template - norm template for quick appontments without exam
- [ ] hash tables (key-value dict)
- [ ] Fuzzy matching / RapidFuzz
- [ ] normalization (comparing Vosk and Whisp chunks)
- [ ] whisp small and base separation (terms and abbrevations) (?) -> or beam size one and focus on hash tables
- [ ] ANONYMIZATION
- [ ] massive refferals - quick and  thorough
- [ ] structured outputs
- [ ] evidence
- [ ] few-shot prompting
- [ ] UI
- [ ] RPA
- [ ] study some libraries...
- [ ] OPTIMIZATION
- [ ] hotkeys
- [ ] sla
- [ ] autoreplacement or a ready made protocol
- [ ] Client-Worker split / Raspberry Pi
- [ ] highlighting empty columns
- [ ] *Flexible Output & Hotkey Snippets
- [ ] 


# md-amb-scribe — Roadmap

## Phase 0: Sandbox & Tech Stack Validation
### Audio & VAD Testing
- [ ] `sounddevice` vs `pyaudio` (mic capture benchmarking)
- [ ] `webrtcvad` vs `silero vad` (silence trimming & speech detection)
- [ ] noise reduction
- [ ] chunks + VAD

### LLM & Structured Output Testing
- [ ] `llama-cpp` + `gguf` (local inference setup)
- [ ] `gbnf` vs `outlines` vs `instructor` (enforcing strict JSON schemas)
- [ ] `few-shot prompting`
- [ ] structured outputs
- [ ] study some libraries...

### Environment & Storage
- [ ] Target OS selection (Windows vs Linux)
- [ ] `sqlite` (local storage setup)

---

## Phase 1: Core MVP (Basic Working Pipeline)
### Audio & Realtime Pipeline
- [ ] streaming
- [ ] realtime pipeline
- [ ] 2 flows (lambda)
- [ ] timestops

### Text Normalization & Dictionaries
- [ ] `initial_prompt:` + Doctor Onboarding Script (`dict_json` and `examples.txt`)
- [ ] hash tables (key-value dict)
- [ ] Fuzzy matching / RapidFuzz
- [ ] stopword filtering
- [ ] autoreplacement or a ready made protocol

### Templates & Extraction
- [x] JSON extraction
- [ ] `default_template` - norm template for quick appointments without exam

---

## Phase 2: Doctor UX, Security & EHR Integration
### Privacy & Clinical Safety
- [ ] ANONYMIZATION
- [ ] evidence

### Document Generation & Complex Cases
- [ ] massive referrals - quick and thorough
- [ ] `docxtpl` vs `html to pdf` (document export)

### UI & Automation (RPA)
- [ ] UI
- [ ] highlighting empty columns
- [ ] hotkeys
- [ ] *Flexible Output & Hotkey Snippets
- [ ] RPA (`pynput` / `xdotool` in Linux)

---

## Phase 3: Advanced Optimization & Scaling
### Hybrid STT & Speed Tuning
- [ ] normalization (comparing Vosk and Whisp chunks)
- [ ] whisp small and base separation (terms and abbreviations) (?) -> or beam size one and focus on hash tables
- [ ] OPTIMIZATION

### Architecture & Reliability
- [ ] Client-Worker split / Raspberry Pi
- [ ] sla





