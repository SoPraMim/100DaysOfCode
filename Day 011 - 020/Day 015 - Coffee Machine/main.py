def main():
    # Imports
    from GenericFunctions import cls
    from support_data import MENU,resources,coins
    
    # Global Variables
    money = 0
    
    # Functions
    def get_user_instruction(text):
        """Checks user input and returns it when it matches"""
        valid_input = list(MENU.keys())
        valid_input.extend(["off","report"])
        while True:
            user_input = input(text).lower()
            if user_input in valid_input:
                return user_input
            else: 
                print("Wrong input. Please try again.")
    
    def get_money_inserted():
        value_inserted = 0
        print("Please insert coins")
        for coin_type in coins:
            while True:
                try:
                    number_coins = int(input(f"How many {coins[coin_type]['plural']}: "))
                    value = number_coins * coins[coin_type]['value']
                    value_inserted += value
                    break
                except:
                    print("Wrong input. Try again")
        return value_inserted
    
    # Software
    cls()
    machine_turned_on = True
    while machine_turned_on:
        #Get user input
        user_instruction = get_user_instruction("What would you like? (espresso/latte/cappuccino):")
        
        # Turn off machine.
        if user_instruction == "off": 
            break
        
        # Print report
        if user_instruction == "report": 
            for resource in resources:
                print(f"{resource.title()}: {resources[resource]['amount']} {resources[resource]['unit']}")
                if money > 0:
                    print(f"Money: ${money}")
            continue
                    
        # Check resources
        for resource in resources:
            if MENU[user_instruction]["ingredients"][resource] > resources[resource]["amount"]:
                print(f"Sorry there is not enough {resource}.")
            continue
        
        # Process coins
        money_inserted = get_money_inserted()
        # Return money if not enough
        if money_inserted < MENU[user_instruction]["cost"]:
            print("Sorry, that's not enough money. Money refunded.")
            continue
        
        # Return change.
        money += MENU[user_instruction]["cost"]
        change = round(money_inserted - MENU[user_instruction]["cost"],2)
        if change > 0:
            print("Here is $%.2f in change" %(change))
            
        # Make coffee
        for resource in resources:
            resources[resource]["amount"] -= MENU[user_instruction]["ingredients"][resource]
        input(f"Here is your {user_instruction}. Enjoy!")
        cls()

if __name__ == "__main__":
    main()