from turtle import Turtle
from typing import Any
import os

FONTNAME = "Arial"
FONTSIZE = 16
FONTTYPE = "normal"
SCOREBOARD_POSITION = (0,260)

GAMEOVER_FONTNAME = ["Arial","Arial"]
GAMEOVER_FONTSIZE = [54,40]
GAMEOVER_FONTTYPE = ["bold","bold"]
GAMEOVER_POSITION = [(0,20), (0,-40)]

ROOT = "Day 021 - 030/Day 021 - Snake complete/"

class Scoreboard(Turtle):
    def __init__(self, shape: str = "classic", undobuffersize: int = 1000, visible: bool = True) -> None:
        """Create the initial scoreboard."""
        super().__init__(shape, undobuffersize, visible)
        self.score = 0
        self.hi_score = 0
        self.read_hi_score()
        self.hideturtle()
        self.penup()
        self.color("white")
                
    def update(self):
        """Update the scoreboard to display the score."""
        self.clear()
        self.goto(SCOREBOARD_POSITION)
        self.write(arg=f"Score: {self.score}   High Score: {self.hi_score}",move=False,align="center",font=(FONTNAME,FONTSIZE,FONTTYPE))
           
    def add_points(self,points):
        """Add points to the current score count."""
        self.score += points
        self.update()
    
    def game_over(self):
        """Show the 'Game Over' screen."""
        self.goto(GAMEOVER_POSITION[0])
        self.write(arg="Game Over",move=False,align="center",font=(GAMEOVER_FONTNAME[0],GAMEOVER_FONTSIZE[0],GAMEOVER_FONTTYPE[0]))
        self.goto(GAMEOVER_POSITION[1])
        self.write(arg=f"Score: {self.score}",move=False,align="center",font=(GAMEOVER_FONTNAME[1],GAMEOVER_FONTSIZE[1],GAMEOVER_FONTTYPE[1]))
    
    def reset_score(self):
        self.score = 0
        
    def update_hi_score(self):
        self.hi_score = self.score
        with open(ROOT + "data.txt","w") as file:
            file.write(str(self.hi_score))
        
    def read_hi_score(self):
        file_path = ROOT + "data.txt"
        try:
            with open(file_path) as file:
                self.hi_score = int(file.read())
        except:
            with open(file_path, "w") as file:
                file.write("0")