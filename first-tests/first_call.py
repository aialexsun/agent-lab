from config import client, MODEL, cost_usd

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": "Ты - саркастичный CFO"},
        {"role": "user", "content": "Объясни Kubernetes в двух предложениях."},
    ],
    temperature=1,
)
print(response.choices[0].message.content)
print(response.usage)
print(f"Cost: ${cost_usd(response.usage):.6f}")