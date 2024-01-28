from tkinter import *
from quiz_brain import QuizBrain
import time

THEME_COLOR = "#375362"
ROOT = "Day 031 - 040/Day 034 - Quiz Game/"

class QuizInterface():
    def __init__(self,quiz_brain: QuizBrain) -> None:
        self.quiz = quiz_brain
        self.window = Tk()
        self.window.title("Quizzler")
        self.window.config(bg=THEME_COLOR,
                           padx=20,
                           pady=20)
        # Labels
        self.score_label = Label(self.window,
                            text="Score: 0",
                            bg=THEME_COLOR,
                            fg="white")
        self.score_label.grid(column=1,
                         row=0)
        
        # Canvas
        self.canvas = Canvas(self.window,
                             width=300,
                             height=250,
                             bg="white",
                             highlightthickness=0)
        self.question_text = self.canvas.create_text(150,125,
                                                     text="[PLACEHOLDER]",
                                                     font=("Ariel",16,"italic"),
                                                     fill=THEME_COLOR,
                                                     width=280)
        self.canvas.grid(column=0,
                            row=1,
                            columnspan=2,
                            pady=50)
        
        # Buttons
        true_image = PhotoImage(file=ROOT+"images/true.png")
        self.true_button = Button(image=true_image,
                                  highlightthickness=0,
                                  command=self.true_button_command)
        self.true_button.grid(row=2, column=0)

        false_image = PhotoImage(file=ROOT+"images/false.png")
        self.false_button = Button(image=false_image,
                                   highlightthickness=0,
                                   command=self.false_button_command)
        self.false_button.grid(row=2, column=1)
        
        # Populate placeholders
        self.get_new_question()
                
        self.window.mainloop()
        
    def get_new_question(self):
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            new_question = self.quiz.next_question()
            self.canvas.itemconfig(self.question_text,text=new_question)
        else:
            self.canvas.itemconfig(self.question_text,text="You've reaced the end of the quiz.")
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")
        
    def update_score(self):
        self.score_label.config(text=f"Score: {self.quiz.score}"
                                )
    def true_button_command(self):
        check = self.quiz.check_answer(True)
        self.update_score()
        if check:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        self.window.after(1000,func= self.get_new_question)

        
    def false_button_command(self):
        check = self.quiz.check_answer(False)
        self.update_score()
        if check:
            self.canvas.config(bg="green")
        else:
            self.canvas.config(bg="red")
        self.window.after(1000,func= self.get_new_question)
