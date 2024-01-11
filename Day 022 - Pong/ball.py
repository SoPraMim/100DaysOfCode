from turtle import Turtle
from paddle import Paddle
import time
import random


class Ball(Turtle):
    def __init__(self, shape: str = "circle", undobuffersize: int = 1000, visible: bool = True) -> None:
        super().__init__(shape, undobuffersize, visible)
        self.step_size = 5

        self.color("white")
        self.penup()
        self.reset_position()
    
    def move(self):
        self.forward(self.step_size)
        
    def hit_top_wall(self):
        if self.ycor() > 290:
            return True
        else:
            return False
        
    def hit_bottom_wall(self):
        if self.ycor() < -290:
            return True
        else:
            return False
        
    def bounce_from_wall(self):
        if self.heading() < 90:
            new_angle = self.heading() * -1
        elif self.heading() < 180:
            complementary_angle = 180-self.heading()
            new_angle = self.heading() + 2 * complementary_angle
        elif self.heading() < 270:
            inverted_axis = self.heading() - 180
            new_angle = inverted_axis * -1 + 180
        elif self.heading() < 360:
            complementary_angle = 360 - self.heading()
            new_angle = self.heading() + 2 * complementary_angle
        self.setheading(new_angle)

    
    def hit_paddle(self,paddle):
        return abs(paddle.xcor() - self.xcor()) < 20 and abs(paddle.ycor() - self.ycor()) < 60
    
    def bounce_from_paddle(self):
        if self.heading() < 90:
            angle_to_add = 90 - self.heading()
            new_angle = self.heading() + 2 * angle_to_add
        elif self.heading() < 180:
            angle_to_subract = self.heading() - 90
            new_angle = self.heading() - 2 * angle_to_subract 
        elif self.heading() < 270:
            angle_to_add = 270 - self.heading()
            new_angle = 270 + angle_to_add
        elif self.heading() < 360:
            angle_to_subract = self.heading() - 270
            new_angle = self.heading() - 2 * angle_to_subract
        self.setheading(new_angle + random.randint(-10,10))
        self.step_size += 1
        
    def reset_position(self):
        self.goto((0,0))
        orientation = random.randint(-60, 60)+180*random.randint(0,1)
        self.setheading(orientation)
        self.step_size = 5


