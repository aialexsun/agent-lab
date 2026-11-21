"""Cloud cost tools shared by the MCP server and the LangGraph agent."""
import csv
from pathlib import Path

PRICES_FILE = Path(__file__).parent / "prices.csv"
# Made-up demo rates: units of each currency per 1 USD.
RATES = {"USD": 1.0, "EUR": 0.92, "CUR": 10.0}


def lookup_price(service: str, size: str) -> float:
    """Return the monthly price in USD for a cloud service and size.

    service: vm, postgres or storage. size: small, medium, large or 100gb.
    """
    with open(PRICES_FILE, newline="") as f:
        for row in csv.DictReader(f):
            if row["service"] == service.lower() and row["size"] == size.lower():
                return float(row["usd_per_month"])
    raise ValueError(f"No price for {service} {size}.")


def sum_costs(items: list[dict]) -> float:
    """Add up monthly costs. Each item has name, unit_price (USD) and quantity."""
    return sum(item["unit_price"] * item["quantity"] for item in items)


def convert_currency(amount: float, from_cur: str, to_cur: str) -> float:
    """Convert an amount between USD, EUR and CUR."""
    usd = amount / RATES[from_cur.upper()]
    return round(usd * RATES[to_cur.upper()], 2)
