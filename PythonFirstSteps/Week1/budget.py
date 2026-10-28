GOAL_USD = 5000
GREEN = "\033[32m"
RESET = "\033[0m"


def main():
    CATEGORIES = ["essentials", "clothes", "transport", "accommodation", "subscriptions", "hobbies", "health", "leisure"]

    total_cur = 0
    for category in CATEGORIES:
        total_cur += ask(category)

    rate = ask_number("Current exchange rate, CUR per 1 USD: ")

    total_usd = to_usd(total_cur, rate)

    print(GREEN + "-" * 40)
    print(f"Total: {total_cur:,.0f} CUR ≈ ${total_usd:,.0f} a month")
    if total_usd > GOAL_USD:
        print(f"Warning: ${total_usd - GOAL_USD:,.0f} above your ${GOAL_USD:,} income target")
    else:
        print(f"Saving ≈ ${GOAL_USD - total_usd:,.0f} a month at ${GOAL_USD:,} income")
    print("-" * 40 + RESET)


def ask(category):
    return ask_number(f"Monthly cost of {category}, CUR: ")


def ask_number(prompt):
    answer = input(prompt)
    answer = answer.replace(" ", "").replace(",", ".")
    return float(answer)


def to_usd(amount, rate):
    return amount / rate


if __name__ == "__main__":
    main()



#git add .
#git commit -m "message"
#git push