from turtle import Turtle
import random

class Food(Turtle):
    def __init__(self, shape="circle"):
        super().__init__(shape)
        self.penup()
        self.shapesize(stretch_len=0.5,stretch_wid=0.5)
        self.color("orange")
        self.speed(10)
        self.goto((random.randint(-14,14)*20,random.randint(-14,14)*20))
        
    def refresh_position(self):
        self.goto((random.randint(-14,14)*20,random.randint(-14,14)*20))