# Imports
from turtle import Turtle

# Global Variables
INITIAL_SIZE = 3
MOVE_DISTANCE = 20

class Snake():
    def __init__(self):
        self.snake_segments=[]
        self.create_snake(INITIAL_SIZE)
        self.head = self.snake_segments[0]

    def create_snake(self,INITIAL_SIZE):
        for i in range(INITIAL_SIZE):
            snake_piece = Turtle(shape="square")
            snake_piece.penup()
            snake_piece.setpos(0-i*MOVE_DISTANCE,0)
            snake_piece.color("white")
            self.snake_segments.append(snake_piece)
            
    def move_forward(self):
        for i in range(len(self.snake_segments)-1,0,-1):
            self.snake_segments[i].goto(self.snake_segments[i-1].pos())
        self.head.forward(MOVE_DISTANCE)
    
    def heading(self):
        return self.head.heading()
    
    def set_orientation_up(self):
        if self.snake_segments[1].ycor() != self.head.ycor() + MOVE_DISTANCE :
            self.head.setheading(90)
        
    def set_orientation_right(self):
        if self.snake_segments[1].xcor() != self.head.xcor() + MOVE_DISTANCE :
            self.head.setheading(0)
        
    def set_orientation_down(self):
        if self.snake_segments[1].ycor() != self.head.ycor() - MOVE_DISTANCE :
            self.head.setheading(270)
        
    def set_orientation_left(self):
        if self.snake_segments[1].xcor() != self.head.xcor() - MOVE_DISTANCE :
            self.head.setheading(180)
        
    def is_in_screen(self):
        x,y = self.head.pos()
        if x <= -300 or x >= 300 or y <= -300 or y >= 300:
            return False
        else: 
            return True