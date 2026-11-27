from config import client, MODEL, cost_usd
question = input("You: ")
response = client.chat.completions.create(
    model=MODEL,
    messages=[
        #{"role": "system", "content": "Ты - саркастичный CFO"},
        #{"role": "user", "content": "Explain Kubernetes in two sentences."},
        {"role": "user", "content": question},
    ],
    temperature=1,
)
print("AI: " + response.choices[0].message.content)
print(response.usage)
print(f"Cost: ${cost_usd(response.usage):.6f}")