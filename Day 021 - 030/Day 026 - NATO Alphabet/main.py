# student_dict = {
#     "student": ["Angela", "James", "Lily"], 
#     "score": [56, 76, 98]
# }

# #Looping through dictionaries:
# for (key, value) in student_dict.items():
#     #Access key and value
#     pass

# # import pandas
# # student_data_frame = pandas.DataFrame(student_dict)

# #Loop through rows of a data frame
# for (index, row) in student_data_frame.iterrows():
#     #Access index and row
#     #Access row.student or row.score
#     pass

# Keyword Method with iterrows()
# {new_key:new_value for (index, row) in df.iterrows()}

# 1. Create a dictionary in this format:
#{"A": "Alfa", "B": "Bravo"}
import pandas as pd

ROOT = "Day 021 - 030\Day 026 - NATO Alphabet/"

data = pd.read_csv(ROOT + "nato_phonetic_alphabet.csv")
nato_alphabet = {row.letter:row.code for (_,row) in data.iterrows()}
# print(nato_alphabet)

# 2. Create a list of the phonetic code words from a word that the user inputs.
def create_phonetic():
    try:
        user_input = input("Enter a word: ").upper()
        output = [nato_alphabet[letter] for letter in user_input]
    except KeyError:
        print("Sorry. Only letters in the alphabet, please.")
        create_phonetic()
    else:
        print(output)

create_phonetic()
