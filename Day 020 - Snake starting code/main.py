def main():
    # Imports
    from turtle import Screen
    from snake import Snake
    from food import Food
    import time
    
    # Global variables/objects
    screen = Screen()
    GAME_STATE = True
    INITIAL_SPEED = 9


    # Functions
    def quit():
        global GAME_STATE
        GAME_STATE = False
    
    # Screen
    screen.setup(width=600, height = 600)
    screen.bgcolor("black")
    screen.title("Snake")
    screen.tracer(0)
    


    # Initialize program   
    snake = Snake()
    food = Food()
    screen.update()

    # Listeners
    screen.listen()
    screen.onkeypress(fun=quit,key="C")
    screen.onkeypress(fun=snake.set_orientation_up,key="w")
    screen.onkeypress(fun=snake.set_orientation_right,key="d")
    screen.onkeypress(fun=snake.set_orientation_down,key="s")
    screen.onkeypress(fun=snake.set_orientation_left,key="a")
    
    screen.onkeypress(fun=snake.set_orientation_up,key="Up")
    screen.onkeypress(fun=snake.set_orientation_right,key="Right")
    screen.onkeypress(fun=snake.set_orientation_down,key="Down")
    screen.onkeypress(fun=snake.set_orientation_left,key="Left")
    
    # Game
    GAME_STATE = True
    while snake.is_in_screen() and GAME_STATE:
        snake.move_forward()
        time.sleep(1-INITIAL_SPEED/10)
        screen.update()
        print(snake.snake_segments[0].pos())
        print(snake.is_in_screen())
        
    
    # Terminate
    screen.exitonclick()
    

if __name__ == "__main__":
    main()