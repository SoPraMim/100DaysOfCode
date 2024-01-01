def main():
    from GenericFunctions import cls
    from figures import logo
    cls()
    print(logo)
    print("\nWelcome to Blind Auction.")
    input("Press Enter to continue.\n")
    
    global list_of_bids
    auction = True
    while auction:
        # Get all bids
        list_of_bids=[]
        while True: # loop to get more bids.
            cls()
            get_bid()
            while True: #checking input from more_bidders.
                more_bidders = input("Are there any more bidders? (Y/N)\n").lower()
                if more_bidders in "yn" and len(more_bidders) == 1:
                    break
            if more_bidders == "n":
                break

        cls()
        # Get the value for the highest bidder and the name(s) of the winner(s).
        highest_value = 0
        winners = []
        for i in range(len(list_of_bids)):
            if list_of_bids[i]["value"] > highest_value:
                highest_value = list_of_bids[i]["value"]
                winners = [list_of_bids[i]["name"]]
            elif list_of_bids[i]["value"] == highest_value:
                winners.append(list_of_bids[i]["name"])
        if len(winners) == 1:
            print(f"The auction winner is {winners[0]} with a value of {highest_value} €.")
        else:
            print(f"The auction winners are {', '.join(winners)} with a value of {highest_value}")
            
            
        # End the auction.
        while True:
            new_auction = input("\n\nDo you want to start a new auction? (Y/N)\n").lower()
            if new_auction in "yn" and len(new_auction) == 1:
                break
        if new_auction == "n":
            auction = False
            print("\nThank you for using Blind Auction.")
            input("Press Enter to quit.")
            cls()
        
    
def get_bid():
    bid = {}
    bid["name"] = input("What is your name? ")
    while True:
        try:
            bid["value"] = int(input("What is your bid? €"))
            break
        except:
            print("Your input should be a number.\n")
    list_of_bids.append(bid)

if __name__ == "__main__":
    main()