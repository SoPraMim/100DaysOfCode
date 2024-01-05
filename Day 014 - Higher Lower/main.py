def main():
    # Imports
    from GenericFunctions import cls, set_y_or_n
    from figures import logo, vs
    from game_data import data
    import random
        
    # Functions
    def set_game_display(entity_1,entity_2,score):
        cls()
        print(logo)
        if score > 0:
            print(f"You're right! Current score: {score}.")
        print(f"Compare A: {entity_1['name']}, a {entity_1['description'].lower()} from {entity_1['country']}.")
        print(vs)
        print(f"Against B: {entity_2['name']}, a {entity_2['description'].lower()} from {entity_2['country']}.\n")
        
    def set_game_over_display(score):
        cls()
        print(logo)
        print(f"Sorry, that wrong. Final Score: {score}")
    
    def get_a_or_b(text):
        """Check the user input if 'a' or 'b' and return the value."""
        while True:
            user_input = input(text).lower()
            if user_input in "ab" and len(user_input) == 1:
                return user_input
            else:
                print("Wrong input. Try again.")

    def who_has_more_followers(entity_1, entity_2):
        if entity_1["follower_count"] >= entity_2["follower_count"]:
            return 'a'
        else:
            return 'b'
    # Welcome Screen
    cls()
    print(logo)
    input("Welcome to the Higher or Lower game.\nPress Enter to start")
    cls()
    
    # Start the game
    # Get the 1st person
    entity_a = random.choice(data)
    
    score=0
    ongoing_game = True
    while ongoing_game:
        # Get the 2nd person
        while True:
            entity_b = random.choice(data)
            if entity_b != entity_a:
                break
        # Update the display
        set_game_display(entity_a,entity_b,score)
        
        # Check user input
        user_answer = get_a_or_b("Who has more followers? Type 'A' or 'B': ")
        
        # Check the result and update counter
        correct_answer = who_has_more_followers(entity_a, entity_b)
        if user_answer == correct_answer:
            score += 1
            entity_a = entity_b
        else:
            ongoing_game = False
        
    # Game over screen
    set_game_over_display(score)
    # back to main menu

    if set_y_or_n("\nDo you want to play again? (Y/N)\n"):
        main()
    else:
        cls()
        print("Thank you for playing Higher or Lower.")
        input()
        cls()
    
if __name__ == "__main__":
    main()