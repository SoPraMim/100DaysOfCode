from GenericFunctions import cls, alphabet
from figures import logo

def main():
    cls()
    print(logo)
    print("\nWelcome to Caeser Cipher.")
    input("Press Enter to continue.\n")
    
    start = True
    while start == True:
        cls()
        [direction,text,shift] = get_input()
        
        if direction == "encode":
            print(f"Your encoded message is:\n{''.join(cypher(text,shift,direction))}")
        else:
            print(f"Your decoded message is:\n{''.join(cypher(text,shift,direction))}")
        
        while True:
            restart = input("\nDo you want to continue? (Y/N)").lower()
            if restart in "yn" and len(restart) == 1:
                break
        if restart == "n":
            start = False
            print("Thank you for using Caeser Cipher.")


def get_input():
    while True:
        direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n").lower()
        if direction not in ["encode","decode"] and len(direction) != 6:
            print("Wrong input.")
        else:
            break
    text = input("Type your message:\n").lower()
    while True:
        try:
            shift = int(input("Type the shift number:\n"))
            break
        except:
            print("Please type the shift size.")
    return [direction,text,shift]
            
def cypher(text,shift,direction):
    new_text=[]
    for letter in text:
        if letter not in alphabet:
            new_text.append(letter)
        else:
            if direction == "encode":
                new_index = (alphabet.index(letter)+shift)%len(alphabet)
            elif direction == "decode":
                new_index = (alphabet.index(letter)-shift)%len(alphabet)
            #print(f"the old index is {alphabet.index(letter)} and the new one is {new_index}")
            new_text.append(alphabet[new_index])
    return new_text

if __name__ == "__main__":
    main()