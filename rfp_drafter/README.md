# RFP Answer Drafter

Drafts structured answers to RFP questions with a local LLM.
Each answer has a short text, a confidence score, assumptions and risks,
validated with Pydantic.

## How it works
1. Reads questions from 'questions.txt'
2. Sends each one to a local model (Ollama) with a JSON schema
3. Validates the reply with Pydantic and retries once if it's invalid
4. Saves everything to 'answers.json' with tokens and timing

## Run
```powershell
uv run python -m rfp_drafter.rfp
```

## Example output
Loaded 5 questions

[1/5] Describe your approach to disaster recovery for a managed PostgreSQL database?
    OK in 33 s, 497 tokens out, confidence 90%

[2/5] How do you ensure data is encrypted at rest and in transit?
    OK in 25 s, 395 tokens out, confidence 95%

[3/5] What is your SLA for managed Kubernetes, and what happens if it is breached?
    OK in 26 s, 433 tokens out, confidence 95%

[4/5] What services do you have that provide some form of protected connection between a cloud and our own datacenter?
    OK in 33 s, 483 tokens out, confidence 95%

[5/5] How can we optimize our cloud resources usage?
    OK in 21 s, 364 tokens out, confidence 80%

## Results
| Model | Valid answers | Avg time per answer | Avg tokens per answer |
|:-:|:-:|:-:|:-:|
| qwen3:8b | 5/5 | 20 s | 448 |
| qwen3:4b | 5/5 | 73 s | 1328 |

## Limitations
- Generic questions only; answers need expert review
- Model confidence is self-reported, not a measured score