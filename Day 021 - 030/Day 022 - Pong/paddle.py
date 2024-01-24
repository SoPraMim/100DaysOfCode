from turtle import Turtle
import time

REFRESH_RATE = 0.03
STEP_SIZE = 20

class Paddle(Turtle):
    def __init__(self,  position = (0,0), shape: str = "classic", undobuffersize: int = 1000, visible: bool = True) -> None:
        super().__init__(shape, undobuffersize, visible)
        self.moving = False
        self.penup()
        self.color("white")
        self.shape("square")
        self.shapesize(stretch_len=4)
        self.setheading(90)
        self.speed(10)
        self.goto(position)
        
    # def stop_moving(self):
    #     self.moving = False
        
    def move_up(self):
        if self.ycor() < 250:
            self.forward(STEP_SIZE)
            
    def move_down(self):
        if self.ycor() > -250:
            self.backward(STEP_SIZE)

