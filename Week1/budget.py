def main():
    #Define constants
    goal = 5000
    
    #Input from user
    ess = float(input("Monthly cost of essentials(food, consumables)? RUB: "))
    cloth = float(input("Monthly cost of clothes? RUB: "))
    transp = float(input("Monthly cost of transport? RUB: "))
    appart = float(input("Monthly cost of accomodation? RUB: "))
    subscr = float(input("Monthly cost of subscriptions (mob, Internet)? RUB: "))
    hobby = float(input("Monthly cost of hobbies? RUB: "))
    med = float(input("Monthly cost of medical services? RUB: "))
    fun = float(input("Monthly cost of leisure? RUB: "))
    rate = float(input("What is current RUB/USD rate? RUB: "))

    total_rub = ess + cloth + transp + appart + subscr + hobby + med + fun
    total_usd = to_usd(total_rub, rate)

    print(f"{"\033[32m"}----------------------")
    if total_usd > goal:
        print(f"!Warning! Your expenses are above the budget of ${goal:,}!")
    else:
        print(f"Total: {round(total_rub):,} RUB ≈ ${round(total_usd):,}. Saving ≈ ${round(goal-total_usd):,} a month at ${goal:,} income. .")
    print(f"----------------------{"\033[0m"}")

def to_usd(sum, rate):
    return sum / rate

if __name__ == "__main__":
    main()