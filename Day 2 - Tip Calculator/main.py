def main():
    print("Welcome to the tip calculator.")
    bill = float(input("What was the total bill? $"))
    Tip_perc = int(input("What percentage tip would you like to give? 10, 12, or 15? "))
    if Tip_perc not in [10,12,15]: #Checks for wrong value input.
        raise ValueError
    nPeople = int(input("How may people to split the bill? "))
    cost_total = bill + bill * Tip_perc / 100
    cost_perPerson = cost_total / nPeople
    print("Each person should pay: $%.2f" %round(cost_perPerson,2))


if __name__ == "__main__":
    main()