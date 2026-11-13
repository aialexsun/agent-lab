# Week 4: Tool use and a hand-written agent loop

Two small experiments on the way to real AI agents:

1. **`first_tool.py`**: the model calls one Python function (a live exchange rate) and uses the result in its answer.
2. **`cost_agent.py`**: a cloud cost estimator agent with three tools, written as a plain loop in about 100 lines, no framework.

The agent loop: **model → picks a tool → my code runs it → result goes back → model decides again → final answer**, with a limit of 10 steps.

## How to run

Requirements: Python via [uv](https://docs.astral.sh/uv/), a local model in [Ollama](https://ollama.com) with tool support (e.g. `qwen3:8b`), and the packages `openai` and `requests`.

```powershell
ollama pull qwen3:8b
uv add openai requests
uv run python -m week4.first_tool
uv run python -m week4.cost_agent
```

The model and client are set in `config.py`. Ollama exposes an OpenAI-compatible API, so switching to a cloud provider means changing the client settings and the model name.

## The tools

| Tool | What it does | Why it's a tool and not the model's job |
|---|---|---|
| `lookup_price(service, size)` | Reads the monthly USD price from `prices.csv` | The model must never guess prices |
| `sum_costs(items)` | Adds up unit price × quantity for each line item | Models are unreliable at arithmetic |
| `convert_currency(amount, from_cur, to_cur)` | Converts using today's rate from open.er-api.com | Rates change daily; the model's knowledge is out of date |

**Price list:** `prices.csv`, USD per month. Prices are not real, just random values for tests. Storage is priced per GB; 1 TB = 1000 GB.

## Example traces

Check the TESTS.md file

## What I learned (and what broke)

- **The tool description is the most important line.** The model picks tools by reading it. Vague descriptions led to wrong or missing calls. Listing the exact allowed values ("One of: vm, postgres, storage_gb, load_balancer") fixed it.
- **The model never runs code.** It only asks; my code runs the function and sends the result back.
- **Small models need explicit instructions.** With tools available and no system prompt, the model refused to answer "What is the capital of France?" because "the tools are for currency conversion". One line in the system prompt fixed it: use a tool only when needed.
- **Units aren't obvious to a model.** It couldn't turn "1 TB" into 1000 × `storage_gb` until the system prompt said "1 TB = 1000 GB".
- **Right answer, wrong reason.** The model sent all three tool calls at once, before seeing any results, and invented a storage price of 0.02. In the next step it saw the real price (0.05), ignored its own tool results and recalculated in its head. The final answer was correct, but the maths wasn't done by the tools. Fix: one tool call per step, enforced in code. I only caught this because the script prints every step.

## Known limitations

- Prices come from a small, static CSV, not a live pricing API.
- Exchange rates from a free public API, updated about once a day.
- Tested only with a small local model; larger models plan better.

## Next

Week 5: wrap these tools in an **MCP server** and rebuild the agent with **LangGraph** to see what a framework adds.
