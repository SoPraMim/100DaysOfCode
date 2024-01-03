rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

def printMove(move):
    if move == "rock":
        print(rock)
    elif move == "paper":
        print(paper)
    elif move == "scissors":
        print(scissors)
        
def checkWinner(player1_move,player2_move):
    if player1_move == "rock":
        if player2_move == "rock":
            return 0
        elif player2_move == "paper":
            return 2
        elif player2_move == "scissors":
            return 1
        else:
            print("Wrong move input")
            
    if player1_move == "paper":
        if player2_move == "rock":
            return 1
        elif player2_move == "paper":
            return 0
        elif player2_move == "scissors":
            return 2
        else:
            print("Wrong move input")

    if player1_move == "scissors":
        if player2_move == "rock":
            return 2
        elif player2_move == "paper":
            return 1
        elif player2_move == "scissors":
            return 0
        else:
            print("Wrong move input")