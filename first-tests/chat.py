from openai import APIConnectionError
from config import client, MODEL

messages = [{"role": "system", "content": "You are a helpful cloud presales architect."}]
token_count = 0

while True:
    user_text = input("You: ")
    if user_text.lower() in ("exit", "quit"):
        break
    if not user_text.strip():
        continue
    messages.append({"role": "user", "content": user_text})
    
    #response = client.chat.completions.create(model=MODEL, messages=messages)
    #answer = response.choices[0].message.content
    #messages.append({"role": "assistant", "content": answer})
    #print(f"AI: {answer}\n[{response.usage.total_tokens} tokens so far in this turn]\n")

    stream = client.chat.completions.create(
        model=MODEL, 
        messages=messages, 
        temperature=1, 
        stream=True, 
        stream_options={"include_usage": True}
    )
    full_answer = ""
    print("AI: ", end="")
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            text = chunk.choices[0].delta.content
            print(text, end="", flush=True)
            full_answer += text
        if chunk.usage:
            token_count += chunk.usage.total_tokens
    print("")
    print("----------------------")
    print(f"Token usage in this session: {token_count} tokens.")
    print("----------------------")
    messages.append({"role": "assistant", "content": full_answer})