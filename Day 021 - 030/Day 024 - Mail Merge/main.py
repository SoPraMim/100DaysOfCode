PLACEHOLDER = "[name]"
ROOT = "Day 021 - 030/Day 024 - Mail Merge/"
        
with open(ROOT + "Input/Letters\starting_letter.txt") as file:
    letter = file.read()

with open(ROOT + "Input/Names/invited_names.txt") as file:
    names = file.readlines()

for name in names:
    name = name.strip()
    with open(ROOT + "Output/ReadyToSend/" + name + ".txt", "w") as new_file:
        new_file.write(letter.replace(PLACEHOLDER, name))