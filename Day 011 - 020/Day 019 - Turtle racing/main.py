def main():
    # Imports
    from turtle import Turtle, Screen
    import random

    # Global variables/objects
    n_turtles = 6
    turtle_size = 3
    turtle_spacing = 10
    screen = Screen()
    colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    starting_x = -100
    ending_x = 100
    
    # Functions
    def create_turtles():
        turtles = []
        for i in range(n_turtles):
            idx = i % len(colors)
            turtle = Turtle(shape="turtle")
            turtle.turtlesize(turtle_size)
            turtle.color(colors[idx])
            turtle.penup()
            turtle.setposition(starting_x,-(n_turtles/2)*turtle_spacing+i*turtle_spacing)
            turtles.append(turtle)
        return turtles

    def start_race():
        is_race_on = True   
        while is_race_on:
            for turtle in turtles:
                turtle.forward(random.randint(0,10))
                pos=turtle.pos()
                if pos[0] >= ending_x:
                    winner,_ = turtle.color()
                    is_race_on = False
        return winner
    
    # Program
    screen.setworldcoordinates(starting_x-turtle_spacing/2,-(n_turtles/2)*turtle_spacing-turtle_spacing/2,ending_x,(n_turtles/2)*turtle_spacing-turtle_spacing/2)    
    turtles = create_turtles()

    # Get the userbet
    while True:
        bet = screen.textinput(title="Make your bet", prompt="Which turtle will win the race? Enter a color;")
        if bet in colors or bet is None:
            break
        
    if bet is not None:
        winner = start_race()
        if bet == winner:
            print("Congrats! You guessed the winner!")
        else:
            print(f"Sorry. The winner was {winner}. Good luck next time!")
    else:
        pass

    

    screen.exitonclick()

if __name__ == "__main__":
    main()