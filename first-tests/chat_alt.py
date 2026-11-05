from openai import APIConnectionError
from config import client, MODEL, cost_usd

messages = [{"role": "system", "content": "You are a helpful cloud presales architect."}]
total_cost = 0.0

while True:
    user_text = input("You: ")
    if user_text.lower() in ("exit", "quit"):
        break
    if not user_text.strip():
        continue
    messages.append({"role": "user", "content": user_text})

    try:
        stream = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            stream=True,
            stream_options={"include_usage": True},
        )
        print("AI: ", end="")
        full_answer = ""
        usage = None
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                text = chunk.choices[0].delta.content
                print(text, end="", flush=True)
                full_answer += text
            if chunk.usage:
                usage = chunk.usage
    except APIConnectionError:
        print("\nCan't reach the model. Is Ollama running? Start it and try again.\n")
        messages.pop()
        continue

    print()
    messages.append({"role": "assistant", "content": full_answer})
    if usage:
        total_cost += cost_usd(usage)
        print(f"[this turn: {usage.prompt_tokens} in + {usage.completion_tokens} out tokens | "
              f"conversation cost so far: ${total_cost:.6f}]")
    print()