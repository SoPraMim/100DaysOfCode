def main():
    # Imports
    from figures import logo
    from GenericFunctions import cls, set_y_or_n
    import random

    # Global variables
    min_number = 1
    max_number = 100
    
    # Required functions
    def set_lives():
        """Checks the user input and returns the number of lives to start with."""
        list_difficulties = ["easy","normal","hard"]
        list_lives = [10,7,5]
        print("""Choose a difficulty.
Easy (10 attempts)
Normal ( 7 attempts)
Hard (5 attempts)

""")
        while True:
            difficulty = input().lower()
            if difficulty in list_difficulties:
                break
            else:
                print("I couldn't understand. Choose between 'easy', 'normal' and 'hard'.\n")
        difficulty_index = list_difficulties.index(difficulty)
        return list_lives[difficulty_index]

    def make_guess(text):
        """Check user input and return the guess."""
        while True:
            try:
                user_guess = int(input(text))
                if user_guess < min_number:
                    print("Your guess is below the minimum number. Try again.")
                    continue                
                elif user_guess > max_number:
                    "Your guess is above the maximum number. Try again."
                    continue
                return user_guess # Exit statement
            except:
                print("Please type a full number.")
    
    # Welcome screen
    cls()
    print(logo)
    print("Welcome to The Number Game!")
    input("Press Enter to continue.")
    

    
    # The game
    ongoing_game = True
    while ongoing_game:
        cls()
        lives = set_lives()
        
        cls()
        number = random.randint(min_number,max_number)
        print("Welcome to The Number Game!")
        
        won_game = False
        while not lives == 0 and not won_game:
            print(f"I'm thinking of a number between {min_number} and {max_number}.")
            guess = make_guess(f"You have {lives} attempts remaining to guess the number.\nMake a guess: ")
            if guess > number:
                print("Too high.\nGuess again.")
                lives -= 1
            elif guess < number:
                lives -= 1
                if lives == 0:
                    print("You ran out of guesses. You lose.") # Lose game.
                else:
                    print("Too low.\nGuess again.")
            elif guess == number:
                print(f"You got it! The answer was {number}.\n")
                won_game = True
            
        ongoing_game = set_y_or_n("\nDo you want to start a new game? (Y/N)\n")
        

    
if __name__ == "__main__":
    main()