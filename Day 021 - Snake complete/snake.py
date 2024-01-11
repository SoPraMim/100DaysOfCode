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
    
    def extend(self):
        new_segment = Turtle(shape="square")
        new_segment.penup()
        new_segment.color("white")
        new_segment.goto(self.snake_segments[-1].pos())
        self.snake_segments.append(new_segment)
            
    def move_forward(self):
        for i in range(len(self.snake_segments)-1,0,-1):
            self.snake_segments[i].goto(self.snake_segments[i-1].pos())
        self.head.forward(MOVE_DISTANCE)
        if self.head.xcor() > 290:
            self.head.setx(-280)
        elif self.head.xcor() < -290:
            self.head.setx(280)
        elif self.head.ycor() > 290:
            self.head.sety(-280)
        elif self.head.ycor() < -290:
            self.head.sety(280)
    
    def heading(self):
        return self.head.heading()
    
    def setheading(self,angle):
        self.head.setheading(angle)
        
    def pos(self):
        coordinates = []
        for segment in self.snake_segments:
            coordinates.append(segment.pos())
        return coordinates
    
    def set_orientation_up(self):
        if self.snake_segments[1].ycor() != self.head.ycor() + MOVE_DISTANCE :
            self.setheading(90)
        
    def set_orientation_right(self):
        if self.snake_segments[1].xcor() != self.head.xcor() + MOVE_DISTANCE :
            self.setheading(0)
        
    def set_orientation_down(self):
        if self.snake_segments[1].ycor() != self.head.ycor() - MOVE_DISTANCE :
            self.setheading(270)
        
    def set_orientation_left(self):
        if self.snake_segments[1].xcor() != self.head.xcor() - MOVE_DISTANCE :
            self.setheading(180)
        
    def bit_itself(self):
        for segment in self.snake_segments[1:]:
            if self.head.distance(segment) < 10:
                return True
        else:
            return False
