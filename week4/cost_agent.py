import csv, json, requests
from config import client, MODEL
from pathlib import Path

PRICES_FILE = Path(__file__).parent / "prices.csv"

def lookup_price(service, size):
    service = service.strip().lower()
    size = size.strip().lower()
    with open(PRICES_FILE, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            if row["service"] == service and row["size"] == size:
                return {"service": service, "size": size, "price_usd_month": float(row["price_usd_month"])}
    return {"error": f"No price for {service} / {size}"}

def sum_costs(items):
    # items: list of {"name": ..., "unit_price": ..., "quantity": ...}
    total = sum(item["unit_price"] * item["quantity"] for item in items)
    return {"total_usd_month": round(total, 2)}

def convert_currency(amount, from_cur, to_cur):
    from_cur = from_cur.strip().upper()
    to_cur = to_cur.strip().upper()
    try:
        response = requests.get(f"https://open.er-api.com/v6/latest/{from_cur}", timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("result") != "success":
            raise ValueError("rate service returned an error")
        rate = data["rates"][to_cur]                 # to_cur per 1 from_cur
        return {"amount": round(float(amount) * rate, 2),
                "currency": to_cur,
                "rate": rate,
                "rate_meaning": f"{to_cur} per 1 {from_cur}",
                "source": "open.er-api.com",
                "updated": data.get("time_last_update_utc")}
    except (requests.RequestException, KeyError, ValueError):
        return {"error": f"Couldn't convert {from_cur} to {to_cur}"}


# Tool description for the model (a JSON schema)
tools = [
    {
        "type": "function",
        "function": {
            "name": "lookup_price",
            "description": "Get the price for specific cloud service and size from the file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "service":   {"type": "string", "description": "One of: vm, postgres, storage_gb, load_balancer."},
                    "size": {"type": "string", "description": "One of: small, medium, large, standard"},
                },
                "required": ["service", "size"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "sum_costs",
            "description": "Add up the monthly cost of several line items (unit price x quantity each). Use for every total.",
            "parameters": {
                "type": "object",
                "properties": {
                    "items": {
                        "type": "array",
                        "description": "Line items to add up",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name":       {"type": "string", "description": "e.g. 'vm medium'"},
                                "unit_price": {"type": "number", "description": "USD per month for one unit, from lookup_price"},
                                "quantity":   {"type": "number", "description": "How many units"},
                            },
                            "required": ["name", "unit_price", "quantity"],
                        },
                    },
                },
                "required": ["items"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "convert_currency",
            "description": "Convert a specified amount of first currency into a second currency.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount":   {"type": "number", "description": "Amount of currency to convert from"},
                    "from_cur":   {"type": "string", "description": "Currency to convert from, ISO code, e.g. USD, RUB, EUR"},
                    "to_cur": {"type": "string", "description": "Currency to express the price in (the answer's currency), ISO code, e.g. USD, RUB, EUR"},
                },
                "required": ["amount", "from_cur", "to_cur"],
            },
        },
    },
]

FUNCTIONS = {"lookup_price": lookup_price, "sum_costs": sum_costs, "convert_currency": convert_currency}

SYSTEM = (
    "You are a cloud cost estimator. Always use lookup_price for prices; never guess. "
    "If user asks about storage, he may specify units other than gb (GigaBytes). If he specifies TB, treat it like this: 1TB = 1000GB."
    "Always use sum_costs for totals and convert_currency for currencies. "
    "Call one tool at a time and wait for its result."
    "If a price is missing, say so. Finish with a short breakdown table."
    "All prices in the price list are in USD per month."
)

MAX_STEPS = 10

def run_agent(question):
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": question}]
    for step in range(1, MAX_STEPS + 1):
        response = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
        msg = response.choices[0].message

        if not msg.tool_calls:                       # no more tools: the model is done
            print(f"\n[step {step}] FINAL ANSWER:\n{msg.content}")
            return msg.content

        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [call.model_dump() for call in msg.tool_calls],
        })
        for call in msg.tool_calls:
            name = call.function.name
            try:
                args = json.loads(call.function.arguments or "{}")
                result = FUNCTIONS[name](**args) if name in FUNCTIONS else {"error": f"Unknown tool {name}"}
            except Exception as e:
                args = call.function.arguments
                result = {"error": f"{type(e).name}: {e}"}
            print(f"[step {step}] {name}({args}) -> {result}")
            messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})

    print("Stopped: too many steps")
    return None

if __name__ == "__main__":
    run_agent("Estimate 1 TB of storage in RUB")
