import csv
import json
import requests

CSV_FILE = "budget.csv"
JSON_FILE = "budget.json"
HOME_CURRENCY = "RSD"      # currency of the amounts in the CSV
TARGET_CURRENCY = "USD"    # currency to convert to
RATE_URL = f"https://open.er-api.com/v6/latest/{TARGET_CURRENCY}"
FALLBACK_RATE = 105.0      # HOME_CURRENCY per 1 TARGET_CURRENCY; set a recent real value
WIDTH = 50
GREEN = "\033[32m"
RESET = "\033[0m"


def main():
    rows = read_rows(CSV_FILE)
    if not rows:
        print("No data in the CSV file.")
        return

    by_month = sum_by(rows, "month")
    by_category = sum_by(rows, "category")
    months = len(by_month)
    rate = get_rate()

    averages = {}
    for category, amount in by_category.items():
        averages[category] = amount / months

    print("Spending by month")
    print_table("Month", by_month, sorted(by_month), rate)

    print(f"\nAverage per month over {months} month(s)")
    order = sorted(averages, key=averages.get, reverse=True)
    print_table("Category", averages, order, rate, total=sum(averages.values()))

    save_json(by_month, averages, months, rate, JSON_FILE)
    print(f"Saved to {JSON_FILE}")


def read_rows(path):
    rows = []
    with open(path, encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file):
            rows.append({
                "month": row["date"][:7],      # "2026-10-01" -> "2026-10"
                "category": row["category"],
                "amount": parse_amount(row["amount"]),
            })
    return rows


def parse_amount(text):
    return float(text.replace(" ", "").replace(",", "."))


def sum_by(rows, field):
    totals = {}
    for row in rows:
        key = row[field]
        totals[key] = totals.get(key, 0) + row["amount"]
    return totals


def get_rate():
    try:
        response = requests.get(RATE_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("result") != "success":
            raise ValueError("rate service returned an error")
        return data["rates"][HOME_CURRENCY]
    except (requests.RequestException, KeyError, ValueError):
        print(f"Couldn't get today's rate, using {FALLBACK_RATE} "
              f"{HOME_CURRENCY} per {TARGET_CURRENCY}")
        return FALLBACK_RATE


def print_table(label, amounts, order, rate, total=None):
    print("-" * WIDTH)
    print(f"{label:<20} {HOME_CURRENCY:>13} {TARGET_CURRENCY:>13}")
    print(GREEN + "-" * WIDTH)
    for name in order:
        amount = amounts[name]
        print(f"{name:<20} {amount:>13,.0f} {amount / rate:>13,.0f}")
    print("-" * WIDTH + RESET)
    if total is not None:
        print(f"{'Total':<20} {total:>13,.0f} {total / rate:>13,.0f}")
        print("-" * WIDTH)


def rounded(amounts):
    result = {}
    for key, value in amounts.items():
        result[key] = round(value, 2)
    return result


def save_json(by_month, averages, months, rate, path):
    total_average = sum(averages.values())
    data = {
        "home_currency": HOME_CURRENCY,
        "target_currency": TARGET_CURRENCY,
        "rate": round(rate, 4),
        "months": months,
        "total_by_month": rounded(by_month),
        "average_per_month": {
            "by_category": rounded(averages),
            "total": round(total_average, 2),
            "total_in_target_currency": round(total_average / rate, 2),
        },
    }
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()