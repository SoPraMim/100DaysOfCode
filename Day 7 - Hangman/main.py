word_list = [
    "Elefante",
    "Águia",
    "Leopardo",
    "Golfinho",
    "Canário",
    "Raposa",
    "Gorila",
    "Orangotango",
    "Iguana",
    "Falcão",
    "Koala",
    "Lémure",
    "Pescada",
    "Polvo",
    "Panda",
    "Leopardo",
    "Tigre",
    "Macaco",
    "Morcego",
    "Atum",
    "Iaque",
    "Zebra",
    "Tatu",
    "Abelha",
    "Chimpanzé",
    "Dingo",
    "Borboleta",
    "Hipopótamo"
]

def main():
    import figures
    import random
    
    # Welcome screen
    print(figures.title)
    print("Bem vindo ao Hangman!\nPressiona Enter para continuar.")
    input()
    
    # Choose a word from the word_list.
    chosen_word = [*random.choice(word_list).lower()] # the * unpacks the string into characters.
    # print(f"the solution is {chosen_word}")
    
    # Set initial display
    global display
    global lives
    global hangman
    global letters_used
    
    display = []
    for _ in chosen_word:
        display.append("_")
    lives = 6
    hangman = figures.stages
    letters_used=[]

    printDisplay()
                
    while "_" in display:
        # Get user guess.
        guess=getGuess()
        letters_used.append(guess)
            
        # Check if the guess is correct.
        new_display = display.copy()
        for i in range(len(chosen_word)):
            if chosen_word[i] in "aàãaá":
                letter_to_check = "a"
            elif chosen_word[i] in "eéèê":
                letter_to_check = "e"
            elif chosen_word[i] in "iíìî":
                letter_to_check = "i"
            elif chosen_word[i] in "oóòõô":
                letter_to_check = "o"
            elif chosen_word[i] in "uúùû":
                letter_to_check = "u"
            elif chosen_word[i] in "cç":
                letter_to_check = "c"
            else:
                letter_to_check = chosen_word[i]
                
            if letter_to_check == guess:
                new_display[i] = chosen_word[i]
        if display == new_display: # i.e. No changes were made to the previous display, so the guess is wrong.
            print("\nHipótese errada.\n")
            lives -= 1
        else:
            print("\nBoa jogada!\n")
            display=new_display
        printDisplay()
        if lives == 0:
            break
    if lives > 0:
        print("\nParabéns! Ganhaste!\n")
    else:
        print(f"\nPerdeste. A palavra certa era {''.join(chosen_word)}.\nTenta outra vez.\n")

def getGuess():
    while True:
        guess = input("\nAdivinha uma letra: ").lower()
        if len(guess) != 1:
            print("\nInsere uma única letra")    
        else:
            try:
                int(guess)
                print("\nEscolhe uma letra")
            except:
                if guess in letters_used:
                    print(f"{guess} já foi selecionado. Escolhe outra letra.")
                else:
                    break 

    return guess

def printDisplay():
    print(hangman[lives])
    print(" ".join(display),"\n")
    if len(letters_used) > 0:
        print(f"Letras usadas:\n{' '.join(letters_used)}")

if __name__ == "__main__":
    main()