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





flowchart TD
    subgraph P0 ["Phase 0: Песочница"]
        direction TB
        OS["1. OS | sounddevice/pyaudio | silero/webrtcvad | llama-cpp + gguf | instructor/outlines"]
        CH["2. chunks + VAD | few-shot | structured outputs"]
        DB["3. sqlite + noise reduction + libs"]
        OS --> CH --> DB
    end

    subgraph P1 ["Phase 1: Ядро обработки"]
        direction TB
        CORE["Whisper -> hash table -> RapidFuzz -> stop-words"]
        
        CORE --> A1["Auto-protocol: сбор в буфер"]
        CORE --> C1["Copilot: streaming + realtime (каждые 15-20с)"]
        
        A1 & C1 --> TPL["default template (структура норм / клише)"]
        TPL --> ANON["Anonymization"]
    end

    subgraph P2 ["Phase 2: Интерфейс и интеграция"]
        direction TB
        ANON --> LLM_A["Auto-protocol: LLM (пересказ фактов)"]
        ANON --> LLM_C["Copilot: LLM (подсказки/идеи)"]
        
        LLM_A --> UI_A["UI: старт/стоп + подсветка пустых"]
        LLM_C --> UI_C["UI: оверлей с карточками"]
        
        UI_A --> RPA_A["RPA: авто-печать в МИС / docxtpl"]
        UI_C --> RPA_C["RPA: точечная вставка по клику"]
    end

    subgraph P3 ["Phase 3: Оптимизация"]
        direction TB
        RPA_A & RPA_C --> OPT["1. OPTIMIZATION (whisp small / base)"]
        OPT --> CW["2. Client-Worker split (Raspberry Pi) + normalization"]
        CW --> SLA["3. SLA"]
    end

    DB --> CORE
