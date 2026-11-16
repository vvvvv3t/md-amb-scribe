
- [x] Model selection: `Qwen 2.5 3B` (`Q4_K_M`) over `Llama 3.2 3B` & `Phi-3 Mini`

- [ ] `llama-cpp` + `.gguf` setup. vs `Ollama` (on Qwen2.5-3B Q4_K_M
- [ ] `GBNF` vs `outlines` vs `instructor`
- [ ] `few-shot` prompting + valid JSON check



## Results



| Metric | `llama-cpp` + `GBNF` | `llama-cpp` + `outlines` | `llama-cpp` + `instructor` |
| :--- | :--- | :--- | :--- |
| **Valid JSON rate (%)** | | | |
| **Generation speed (tokens/sec)** | | | |
| **Total response time (sec)** | | | |
| **Peak RAM / VRAM usage (GB)** | | | |
| **Extraction accuracy (no hallucinations)** | | | |
| **Ease of schema setup (1-5)** | | | |



### 


Goal of Experiment 002: Structured Output Enforcement

• Core objective: Find the most reliable and lightweight way to force Qwen 2.5 3B into generating 100% valid JSON with exact schema keys (preventing KeyError crashes during .docx report generation).
• Why it matters: Without strict constraints, small 3B models tend to improvise nested objects instead of flat lists.
• What is being tested (GBNF vs outlines vs instructor):
	• Native GBNF: Fastest and dependency-free, but can occasionally misplace fields in complex lists.
	• outlines: Mathematically blocks invalid tokens during generation, though it may have version conflicts with llama-cpp-python.
	• instructor: Easiest developer experience with automatic retries on failure, but retries add latency on weak hardware.
• Outcome: Measure the speed/RAM overhead of each wrapper and pick one winning tool for the production pipeline (Auto-protocol & Copilot).

