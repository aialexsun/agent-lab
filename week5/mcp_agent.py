"""Your own agent: a local model that uses tools from your MCP server."""
import asyncio
import json

from mcp import Client, StdioServerParameters
from openai import OpenAI

llm = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")  # Ollama ignores the key
MODEL = "qwen3:8b"
SERVER = StdioServerParameters(command="uv", args=["run", "cost_server.py"])
MAX_STEPS = 10


async def run_agent(question: str) -> None:
    async with Client(SERVER) as mcp:
        # 1. Ask the MCP server which tools it has, in the format the model expects.
        listed = await mcp.list_tools()
        tools = [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.input_schema,
                },
            }
            for t in listed.tools
        ]

        # 2. The agent loop from week 4, but tools now run on the MCP server.
        messages = [{"role": "user", "content": question}]
        for step in range(1, MAX_STEPS + 1):
            reply = llm.chat.completions.create(model=MODEL, messages=messages, tools=tools)
            message = reply.choices[0].message
            messages.append(message.model_dump(exclude_none=True))

            if not message.tool_calls:
                print(f"\nAnswer:\n{message.content}")
                return

            for call in message.tool_calls:
                args = json.loads(call.function.arguments)
                print(f"[step {step}] {call.function.name}({args})")
                result = await mcp.call_tool(call.function.name, args)
                text = result.content[0].text
                print(f"          -> {text}")
                messages.append({"role": "tool", "tool_call_id": call.id, "content": text})

        print(f"Stopped after {MAX_STEPS} steps without a final answer.")


if __name__ == "__main__":
    asyncio.run(run_agent("Estimate the monthly cost of 3 medium VMs and a medium Postgres database, in CUR."))
