def main():
    from GenericFunctions import cls
    from figures import logo
    
    cls()    
    # Define basic operations:
    global operations
    operations = {}
    operations["+"] = add
    operations["-"] = subtract
    operations["*"] = multiply
    operations["/"] = divide
                
    def calculation():
        print(logo)

        # Pick the 1st number:
        num1 = getNumber()
        continue_calculations = True
        while continue_calculations:
            # Pick the operation:
            operation_symbol = getOperation()
            
            # Pick the 2nd number:
            num2 = getNumber()
            
            # Make the calculation:
            calculation = operations[operation_symbol]
            answer = calculation(num1,num2)
            
            print(f"{num1} {operation_symbol} {num2} = {answer}\n")
            
            num1 = answer
            while True:
                should_continue = input(f"Type 'y' to continue calculating with {answer}, or type 'n' to exit.\n").lower()
                if should_continue in "yn" and len(should_continue) == 1:
                    break
            if should_continue == "n":
                continue_calculations = False
        while True:
            new_calculation = input("Do you want to start a new function? (Y/N)")
            if new_calculation in "yn" and len(new_calculation)==1:
                break
            if new_calculation == "y":
                calculation()
    
    calculation()
        
def add(n1, n2):
    """Adds two values"""
    return n1 + n2

def subtract(n1, n2):
    """Subtracts the 2nd number from the 1st one."""
    return n1 - n2

def multiply(n1, n2):
    """Multiplies two numbers"""
    return n1 * n2

def divide(n1, n2):
    """Divide the 1st number by the 2nd one."""
    return n1 / n2

def getNumber():
    while True:
        try:
            number = float(input("Pick a number: "))
            break
        except:
            continue
    return number

def getOperation():
    for symbol in operations:
        print (symbol)
    while True:
        operation_symbol = input("Pick an operation from the line above:")
        if len(operation_symbol) == 1 and operation_symbol in "+-*/":
            break
    return operation_symbol
if __name__ == "__main__":
    main()