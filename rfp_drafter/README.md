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
```json
  {
    "question": "Describe your approach to disaster recovery for a managed PostgreSQL database?",
    "answer": "Our approach to disaster recovery for managed PostgreSQL includes regular automated backups using WAL-G for point-in-time recovery, geographic replication for cross-region failover, and failover automation via cloud-native tools. We prioritize testing restore procedures and maintaining redundant, versioned backups in secure storage. Monitoring and alerting ensure timely detection of issues, while a documented DR plan ensures alignment with business continuity requirements.",
    "confidence": 0.92,
    "assumptions": [
      "Managed PostgreSQL service provides backup infrastructure",
      "User has configured retention policies and storage locations",
      "Replication and failover tools are supported by the cloud platform",
      "Disaster scenarios align with standard RTO/RPO targets"
    ],
    "risks": [
      "Backup corruption or incomplete backups may render data unrecoverable",
      "Network latency could delay failover during regional outages",
      "Untested DR plans may fail under real-world conditions",
      "Dependence on cloud provider-specific tools may limit flexibility"
    ],
    "tokens_in": 110,
    "tokens_out": 629,
    "seconds": 29.3
  }
```

## Results
| Model | Valid answers | Avg time per answer | Avg tokens per answer |
|:-:|:-:|:-:|:-:|
| qwen3:8b | 5/5 | 20 s | 448 |
| qwen3:4b | 5/5 | 73 s | 1328 |

## Limitations
- Generic questions only; answers need expert review
- Model confidence is self-reported, not a measured score