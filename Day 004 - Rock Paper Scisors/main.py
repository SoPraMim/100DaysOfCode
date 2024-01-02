import random
import my_module

def main():
    moves = ("rock","paper","scissors")
    user_move = 0
    while user_move == 0:
        user_move = (input("Choose between \"Rock\", \"Paper\", \"Scissors.\n")).lower()
        if user_move not in moves:
            print("You typed a wrong move. Try again.")
            user_move = 0
    print(f"You selected {user_move}")
    my_module.printMove(user_move)    
    
    ai_move = random.randint(0,2)
    ai_move = moves[ai_move]
    print (f"The AI selected {ai_move}.")
    my_module.printMove(ai_move)
    
    winner = my_module.checkWinner(user_move,ai_move)
    if winner == 0:
        print("It was a draw. Try again!")
    elif winner == 1:
        print("Congrats! You won!")
    elif winner == 2:
        print("Oops! You lost. Try again!")
    
        
if __name__ == "__main__":
    main()