PLACEHOLDER = "[name]"
        
with open("Day 24 - Mail Merge/Input/Letters\starting_letter.txt") as file:
    letter = file.read()

with open("Day 24 - Mail Merge/Input/Names/invited_names.txt") as file:
    names = file.readlines()

for name in names:
    name = name.strip()
    with open("Day 24 - Mail Merge/Output/ReadyToSend/" + name + ".txt", "w") as new_file:
        new_file.write(letter.replace(PLACEHOLDER, name))