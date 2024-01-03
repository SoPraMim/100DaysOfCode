from GenericFunctions import cls
def main():
    import figures
    import random
    from words import word_list
    from GenericFunctions import set_y_or_n, alphabet
    
    # Welcome screen
    cls()
    print(figures.title)
    print("Bem vindo ao Hangman!\nPressiona Enter para continuar.")
    input()
    
    # print(f"the solution is {chosen_word}")
    
    # Set initial display
    global display
    global lives
    global hangman
    global letters_used
    global chosen_topic
    
    new_game = True
    while new_game:
        # Choose a word from the word_list.
        keys = list(word_list.keys())
        chosen_topic = random.choice(keys)
        chosen_word = [*random.choice(word_list[chosen_topic]).lower()] # the * unpacks the string into characters.

        cls()
        display = []
        for char in chosen_word:
            #print(char in alphabet)
            #print(char in "àãáéèêíìîóòõôúùûç")
            if not any([char in alphabet,char in "àãáéèêíìîóòõôúùûç"]):
                display.append(char)
            else:
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
        new_game=set_y_or_n("\nQueres continuar a jogar? (Y/N)\n")
    cls()
    input("Obrigado por jogar ao Hangman!")
    cls()

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
    cls()
    print(hangman[lives])
    print(" ".join(display),"\n")
    print(f"Tópico:\n{chosen_topic}\n")
    if len(letters_used) > 0:
        print(f"Letras usadas:\n{' '.join(letters_used)}")

if __name__ == "__main__":
    main()