from GenericFunctions import cls

def main():
    from figures import logo
    import random
    import time
    from GenericFunctions import set_y_or_n
    
    global deck
    global player_hand
    global dealer_hand
    global wallet
    global bet
    
    # Welcome screen
    cls()
    print(logo)
    print("Welcome to SPM's Blackjack.")
    input("Press Enter to continue.")
    
    # Select difficulty and set wallet
    wallet = set_initial_wallet()
    
    # Create deck
    deck = createDeck()
    random.shuffle(deck)
        
    ongoing_game = True
    while ongoing_game:
                
        # Set initial bet
        bet = set_bet()
        
        # Create new deck if needed.
        if len(deck) < 15:
            deck = createDeck()
            random.shuffle(deck)
                
        # Initial hands    
        player_hand = []
        dealer_hand = []
        for _ in range(2):
            player_hand.append(draw_card())
            dealer_hand.append(draw_card())
        
        # Set playing display
        set_playing_display()
        
        # Player move
        while True:
            if get_hand_value(player_hand) < 21:
                keep_drawing = set_y_or_n("Do you want to keep drawing? (Y/N)\n")
                if keep_drawing == True:
                    hit_me()
                elif keep_drawing == False:
                    break
            else: # if the player score is above 21
                break
        final_player_score = get_hand_value(player_hand)
        
        # Dealer Drawing
        time.sleep(1)
        set_result_display()
        while final_player_score <= 21 and get_hand_value(dealer_hand) < 17:
            time.sleep(1)
            dealer_hand.append(draw_card())
            set_result_display()
        
        final_dealer_score = get_hand_value(dealer_hand)
        
        time.sleep(1)
        if (final_player_score <= 21 and final_player_score > final_dealer_score) or (final_player_score <= 21 and final_dealer_score > 21):
            wallet += bet
            print("\nCongratulations. You won.")
            print(f"\nMoney available: {wallet} €")
        elif final_player_score <= 21 and final_player_score == final_dealer_score:
            print("\nIt's a draw.")
            print(f"\nMoney available: {wallet} €")
        else:
            wallet -= bet
            print("\nYou lost.")
            print(f"\nMoney available: {wallet} €")
        
        if wallet > 0:
            ongoing_game = set_y_or_n("Do you want to keep playing? (Y/N)\n")
        else:
            input("You ran out of money. Game Over.\n")
            ongoing_game = False
               
    cls()
    input("Thank you for playing SPM's Blackjack.\n")
    cls()
    
    ############### Blackjack Project #####################

    #Difficulty Normal 😎: Use all Hints below to complete the project.
    #Difficulty Hard 🤔: Use only Hints 1, 2, 3 to complete the project.
    #Difficulty Extra Hard 😭: Only use Hints 1 & 2 to complete the project.
    #Difficulty Expert 🤯: Only use Hint 1 to complete the project.

    ############### Our Blackjack House Rules #####################

    ## The deck is unlimited in size. 
    ## There are no jokers. 
    ## The Jack/Queen/King all count as 10.
    ## The the Ace can count as 11 or 1.
    ## Use the following list as the deck of cards:
    ## cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    ## The cards in the list have equal probability of being drawn.
    ## Cards are not removed from the deck as they are drawn.
    ## The computer is the dealer.

    ##################### Hints #####################

    #Hint 1: Go to this website and try out the Blackjack game: 
    #   https://games.washingtonpost.com/games/blackjack/
   
    
def createDeck():
    """Creates a new deck."""
    deck_symbols = ["Hearts","Diamonds", "Spades","Clubs"]
    deck_values = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    deck = []
    for symbol in deck_symbols:
        for value in deck_values:
            deck.append([value,symbol])        
    return deck

def draw_card():
    """Draw the top card from the deck."""
    card = deck[0]
    deck.pop(0)
    return card

def get_card_value(card):
    """Returns the card value."""
    deck_values = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    card_values = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    value_index = deck_values.index(card[0])
    return card_values[value_index]

def get_hand_value(hand):
    """Returns the total value from all cards in the hand."""
    total_value = 0
    number_aces = 0
    for card in hand:
        total_value += get_card_value(card)
        if card[0] == "A":
            number_aces += 1
    for i in range(number_aces):
        if total_value > 21:
            total_value -= 10
    return total_value    

def hit_me():
    """Lets the player draw another card """
    player_hand.append(draw_card())
    set_playing_display()

def set_initial_wallet():
    """Checks the user input and returns the corresponding value for the wallet."""
    cls()
    while True:
        difficulty=input("""Select the difficulty of the game:\n
Easy (20 €)
Normal (10 €)
Hard (5 €)
\n""").lower()
        if difficulty in ["easy","normal","hard"]:
            break
    if difficulty == "easy":
        wallet = 20
    elif difficulty == "normal":
        wallet = 10
    elif difficulty == "hard":
        wallet = 5
    return wallet

def set_bet():
    """"Checks the input and returns the value for the bet."""
    cls()
    while True:
        try:
            bet = int(input(f"Set your bet. (money available:{wallet} €)\n"))
            if bet > wallet:
                print("Your bet cannot be higher than the money you have.")
                continue
            if bet <= 0:
                print("You cannot make null bets.")
            break
        except:
            print("Please enter a full number.\n")
    return bet

def set_playing_display():
    """Creates a new display with updated details to be used while playing. Hides the 2nd card from the dealer """
    cls()
    print("Your hand:")
    for i in range(len(player_hand)):
        print(f"{' '.join(player_hand[i])}")
    print(f"Total value: {get_hand_value(player_hand)}")
    print("\nDealer's hand:")
    for i in range(len(dealer_hand)):
        if i == 0:
            print(f"{' '.join(dealer_hand[i])}")
        else:
            print("*** ***\n")
    print(f"Current bet: {bet} €")
    print(f"Money remaining: {(wallet-bet)}")

def set_result_display():
    """Creates a new display with updated details to be used while revealing results. """
    cls()
    
    print("Your hand:")
    for i in range(len(player_hand)):
        print(f"{' '.join(player_hand[i])}")
    print(f"Total value: {get_hand_value(player_hand)}")
    print("\nDealer's hand:")
    for i in range(len(dealer_hand)):
        print(f"{' '.join(dealer_hand[i])}")
    print(f"Total value: {get_hand_value(dealer_hand)}\n")
    print(f"Current bet: {bet} €")
    print(f"Money remaining: {(wallet-bet)}")
    
if __name__ == "__main__":
    main()