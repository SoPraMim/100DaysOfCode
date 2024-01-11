def main():
    # Imports
    from menu import Menu, MenuItem
    from coffee_maker import CoffeeMaker
    from money_machine import MoneyMachine
    from GenericFunctions import cls
    
    # Global Variables/Objects
    menu = Menu()
    coffee_maker = CoffeeMaker()
    money_machine = MoneyMachine()
    
    # Functions
    def get_user_instruction(text):
        """Checks user input and returns it when it matches"""
        valid_input = (menu.get_items()).split("/")
        valid_input.pop()
        valid_input.extend(["off","report"])
        while True:
            user_input = input(text).lower()
            if user_input in valid_input:
                return user_input
            else: 
                print("Wrong input. Please try again.") 
                
    # Program
    cls()
    while True:
        user_instruction = get_user_instruction(f"What would you like? ({(menu.get_items())[:-1]}) ")
        if user_instruction == "off":
            break
        if user_instruction == "report":
            coffee_maker.report()
            money_machine.report()
            continue
        
        drink = menu.find_drink(user_instruction)
        
        if not coffee_maker.is_resource_sufficient(drink):
            continue
        
        if not money_machine.make_payment(drink.cost):
            continue
        
        coffee_maker.make_coffee(drink)
        input()
        cls()
        
    
if __name__ == "__main__":
    main()