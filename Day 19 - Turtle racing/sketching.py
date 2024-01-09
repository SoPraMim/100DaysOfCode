from turtle import Turtle,Screen

turtle_the_turtle = Turtle()
screen = Screen()

def move_forward():
    turtle_the_turtle.forward(10)
    
def move_backward():
    turtle_the_turtle.backward(10)
    
def turn_left():
    turtle_the_turtle.left(10)
    
def turn_right():
    turtle_the_turtle.right(10)
    
def turn_pen():
    if turtle_the_turtle.isdown():
        turtle_the_turtle.penup()
    else:
        turtle_the_turtle.pendown()
        
def reset():
    turtle_the_turtle.reset()
    
screen.onkey(key="w", fun=move_forward)
screen.onkey(key="s", fun=move_backward)
screen.onkey(key="a", fun=turn_left)
screen.onkey(key="d", fun=turn_right)
screen.onkey(key="c", fun=reset)


screen.listen()
screen.onkey(key="space", fun=turn_pen)

screen.exitonclick()