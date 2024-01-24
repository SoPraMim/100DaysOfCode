import pandas as pd
import random

ROOT = "Day 031 - 040/Day 031 - Flash Card Game/"

class WordManager:
    def __init__(self,n_words=10,language="Danish") -> None:
        if language.title() not in ["French","Danish"]:
            raise NameError("Input language not available.")
        self.language = language.title()
        self.words = None
        self.current_word = None
        
        self.get_list_of_words(n_words)
        self.get_new_word()
        
    def get_list_of_words(self,n_words):
        words = pd.read_csv(ROOT + "data/" + self.language.lower() + "_words.csv")
        self.words = words[0:n_words-1]
    
    def get_new_word(self):
        self.current_word = self.words.iloc[random.randint(0,self.words.shape[0]-1),:]
        
    def delete_current_word(self):
        self.words = self.words.drop(self.words[(self.words[self.language] == self.current_word[self.language])].index)
    
    def count_words(self):
        return self.words.shape[0]