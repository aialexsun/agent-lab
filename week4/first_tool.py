import json
import requests
from config import client, MODEL


def get_exchange_rate(home_currency, target_currency):
    home_currency = home_currency.strip().upper()
    target_currency = target_currency.strip().upper()

    try:
        rate_url = f"https://open.er-api.com/v6/latest/{target_currency}"
        response = requests.get(rate_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("result") != "success":
            raise ValueError("rate service returned an error")
        return {"rate": data["rates"][home_currency],
            "meaning": f"{home_currency} per 1 {target_currency}",
            "source": "open.er-api.com",
            "updated": data.get("time_last_update_utc")}
    
    except (requests.RequestException, KeyError, ValueError):
        return {"error": f"Couldn't get today's rate of {home_currency} per {target_currency}"}


# Tool description for the model (a JSON schema)
tools = [{
    "type": "function",
    "function": {
        "name": "get_exchange_rate",
        "description": "Get how many units of home currency one unit of a target currency costs. Use for any currency conversion.",
        "parameters": {
            "type": "object",
            "properties": {
                "home_currency":   {"type": "string", "description": "Currency to express the price in (the answer's currency), ISO code, e.g. RUB"},
                "target_currency": {"type": "string", "description": "Currency being priced, ISO code, e.g. EUR"},
            },
            "required": ["home_currency", "target_currency"],
        },
    },
}]


# messages = [{"role": "user", "content": "What is the capital of France?"}]
messages = [
    {"role": "system", "content": "You are a helpful assistant. Use a tool only when it is needed; otherwise answer from your own knowledge."},
    {"role": "user", "content": "What is the capital of France?"},
]

response = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
msg = response.choices[0].message

if msg.tool_calls:
    # keep the model's request in the conversation
    messages.append({
        "role": "assistant",
        "content": msg.content or "",
        "tool_calls": [call.model_dump() for call in msg.tool_calls],
    })
    for call in msg.tool_calls:
        args = json.loads(call.function.arguments)     # arguments arrive as a JSON string
        print(f"Model asked for: {call.function.name}({args})")
        result = get_exchange_rate(**args)
        messages.append({
            "role": "tool",
            "tool_call_id": call.id,
            "content": json.dumps(result),
        })
    final = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
    print(final.choices[0].message.content)

    result = get_exchange_rate(**args)
    print(f"Tool returned: {result}")
else:
    print("Model answered without a tool:", msg.content)