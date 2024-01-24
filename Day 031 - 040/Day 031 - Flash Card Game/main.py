# --- Imports --- #
from tkinter import *
from tkinter import messagebox
from word_manager import WordManager

# --- Global Variables --- #
TITLE = "Flashy"
ROOT = "Day 031 - 040/Day 031 - Flash Card Game/"
BACKGROUND_COLOR = "#B1DDC6"
N_WORDS = 20
LANGUAGE = "Danish"
timer = None

# --- Functions --- #
def set_card_front():
    canvas.itemconfig(card_image, image= img_front)
    canvas.itemconfig(language_text, text= LANGUAGE.title())
    canvas.itemconfig(word_text, text= word_manager.current_word[LANGUAGE.title()])
    global timer
    timer = window.after(3000, set_card_back)
    
def set_card_back():
    canvas.itemconfig(card_image, image= img_back)
    canvas.itemconfig(language_text, text= "English")
    canvas.itemconfig(word_text, text= word_manager.current_word["English"])
    
def wrong_button_command():
    window.after_cancel(timer)
    word_manager.get_new_word()
    set_card_front()
    
def right_button_command():
    window.after_cancel(timer)
    word_manager.delete_current_word()
    if word_manager.count_words() > 0:
        word_manager.get_new_word()
        set_card_front()
    else:
        messagebox.showinfo(TITLE, message="Congrats! You completed all the flash cards!")
        window.destroy()        

# --- Initialization --- #    
word_manager = WordManager(n_words=N_WORDS,language=LANGUAGE)


# --- UI interface --- #
window = Tk()
window.title(TITLE)
window.config(padx=50,
              pady=50,
              bg=BACKGROUND_COLOR)

# Canvas
canvas = Canvas(width=800,
                height=526,
                highlightthickness=0,
                bg=BACKGROUND_COLOR)
img_front = PhotoImage(file= ROOT + "images/card_front.png")
img_back = PhotoImage(file= ROOT + "images/card_back.png")
card_image = canvas.create_image(400, 263, image= img_front)
language_text = canvas.create_text(400,150,
                                   text="PLACEHOLDER",
                                   fill="black",
                                   font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400,263,
                               text="PLACEHOLDER",
                               fill="black",
                               font=("Ariel", 60, "bold"))
canvas.grid(column=0,
            row=0,
            columnspan=2)
set_card_front()


# Buttons
wrong_button_image = PhotoImage(file= ROOT + "images/wrong.png")
wrong_button = Button(window,image=wrong_button_image,
                      highlightthickness= 0,
                      borderwidth= 0,
                      command= wrong_button_command)
wrong_button.grid(column=0,
                  row=1)

right_button_image = PhotoImage(file= ROOT + "images/right.png")
right_button = Button(window,image= right_button_image,
                      highlightthickness= 0,
                      borderwidth= 0,
                      command= right_button_command)
right_button.grid(column=1,
                  row=1)

window.mainloop()