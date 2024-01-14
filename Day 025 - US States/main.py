def main():
    from turtle import Turtle, Screen
    import pandas as pd

    STATES = "C:/Git/100DaysOfCode/Day 025 - US States/50_states.csv"
    IMAGE = "Day 025 - US States/blank_states_img.gif"

    screen = Screen()
    turtle = Turtle()

    screen.setup(725,491)
    screen.addshape(IMAGE)
    turtle.shape(IMAGE)
    turtle.penup()
    screen.tracer(0)

    data = pd.read_csv(STATES)
    print()

    screen.onkey(fun=screen.bye, key="Escape")
    screen.listen()

    states_added = []
    game_is_running = True
    while game_is_running:
        user_guess = screen.textinput(f"States ({len(states_added)}/50)", "Guess a state:")
        if user_guess == None:
            game_is_running = False
            screen.bye()
            break

        if user_guess.title() in data.state.tolist() and user_guess.title() not in states_added:
            states_added.append(user_guess.title())
            x = data[data.state == user_guess.title()].x
            y = data[data.state == user_guess.title()].y
            turtle.goto((int(x),int(y)))
            turtle.write(f"{user_guess.title()}",align="center",font=("Arial",12,"normal"))
        
        if len(states_added) == 50:
            game_is_running = False
            turtle.goto(0,0)
            turtle.write("        Congratulations.\nYou guessed all 50 states!",align="center", font=("Arial",24,"bold"))
            
    missing_states = data.state[~data.state.isin(states_added)]
    print(missing_states)
            
    screen.mainloop()

if __name__ == "__main__":
    main()