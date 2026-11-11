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
