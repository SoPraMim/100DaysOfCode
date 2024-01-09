def main():
    from turtle import Turtle, Screen
    import turtle
    import random

    turtle_the_turtle = Turtle() # My first pet was a turtle named... Turtle.
    
    turtle_the_turtle.shape("turtle") # Just to make it funnier.

    # Challenge 1 - Draw a square
    # for i in range(4):
    #     turtle_the_turtle.right(90)
    #     turtle_the_turtle.forward(100)

    # Challenge 2 - Make a dashed line
    # for i in range(10):
    #     turtle_the_turtle.forward(10)
    #     turtle_the_turtle.penup()
    #     turtle_the_turtle.forward(10)
    #     turtle_the_turtle.pendown()
        
    # Challenge 3 - Draw multiple shapes
    # turtle.colormode(255)
    # for n_sides in range(3,40):
    #     turtle_the_turtle.color((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
    #     for _ in range(n_sides):
    #         turtle_the_turtle.forward(100)
    #         turtle_the_turtle.right(360/n_sides)
    
    # Challenge 4 - Random walk
    # turtle.colormode(255)
    # turtle_the_turtle.pensize(10)
    # turtle_the_turtle.speed(10)
    #
    # steps = 100
    # for _ in range(steps):
    #     turtle_the_turtle.color((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
    #     turtle_the_turtle.setheading(random.choice([0,90,180,270]))
    #     turtle_the_turtle.forward(50)
    
    # Challenge 5 - Spirograph
    # turtle.colormode(255)
    # turtle_the_turtle.speed(10)
    # n_circles = 100
    # for _ in range(n_circles):
    #     turtle_the_turtle.color((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
    #     turtle_the_turtle.circle(100)
    #     turtle_the_turtle.setheading(turtle_the_turtle.heading()+360/n_circles)
    
        

    screen = Screen()
    screen.exitonclick()
    
if __name__ == "__main__":
    main()