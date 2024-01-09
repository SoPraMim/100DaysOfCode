def main():
    # Imports
    import turtle
    import random
    
    # Global variables/objects
    turtle_the_turtle = turtle.Turtle()
    screen = turtle.Screen()

    colors = get_colors("Day 018 - Turtle/image.jpg")
    n_rows = 10
    n_collumns = 10
    spacing = 30
    
    # Program
    turtle.colormode(255)
    turtle_the_turtle.shape("turtle")
    turtle_the_turtle.setheading(0) # Ensure the right orientation
    
    (x_initial,y_initial) = (0,0) # Define the initial position
    
    screen.setworldcoordinates(x_initial-spacing,y_initial-spacing,x_initial+spacing*(n_collumns),y_initial+spacing*(n_collumns)) # Set the field of view.
    turtle_the_turtle.penup()
    
    for r in range(n_rows):
        turtle_the_turtle.setposition(x_initial, y_initial+(r)*spacing)
        for c in range(n_collumns):
            turtle_the_turtle.color(random.choice(colors))
            turtle_the_turtle.stamp()   #This is so much cuter than placing dots...
            turtle_the_turtle.forward(spacing)
    turtle_the_turtle.hideturtle()


    screen.exitonclick()

# Functions
def get_colors(figure):
    import colorgram

    rgb_colors = []
    colors = colorgram.extract(figure, 30)
    for color in colors:
        r = color.rgb.r
        g = color.rgb.g
        b = color.rgb.b
        if sum([r,g,b]) > 650: # This excludes colours too close to the background, i.e. white.
            continue
        rgb_colors.append((r,g,b))
    return rgb_colors
    
if __name__ == "__main__":
    main()