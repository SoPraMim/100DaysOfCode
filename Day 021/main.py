def main():
    # Imports
    from turtle import Screen
    from snake import Snake
    from food import Food
    from scoreboard import Scoreboard
    import time
    
    # Global variables/objects
    screen = Screen()
    INITIAL_LEVEL = 5
    SPEED_INCREASE = 20
     
    # Screen
    screen.setup(width=600, height = 600)
    screen.bgcolor("black")
    screen.title("Snake")
    screen.tracer(0)
    
    # Initialize program   
    snake = Snake()
    food = Food()
    scoreboard = Scoreboard()
    screen.update()
    
    # Listeners
    screen.listen()

    screen.onkeypress(fun=snake.set_orientation_up,key="w")
    screen.onkeypress(fun=snake.set_orientation_right,key="d")
    screen.onkeypress(fun=snake.set_orientation_down,key="s")
    screen.onkeypress(fun=snake.set_orientation_left,key="a")
    
    screen.onkeypress(fun=snake.set_orientation_up,key="Up")
    screen.onkeypress(fun=snake.set_orientation_right,key="Right")
    screen.onkeypress(fun=snake.set_orientation_down,key="Down")
    screen.onkeypress(fun=snake.set_orientation_left,key="Left")
    
    # Game
    level = INITIAL_LEVEL
    interval = 0.5 - (level-1)/10*0.5
    food_count = 0
    game_state = True
    while game_state:
        screen.update()
        time.sleep(interval)
        snake.move_forward()
        # print(snake.snake_segments[0].pos())
        
        # Eating food
        if snake.head.distance(food) < 1:
            food.refresh_position()
            scoreboard.add_points(level)
            snake.extend()
            food_count += 1
            if food_count == 5 and level < 10:
                food_count = 0
                level += 1
                interval = 0.5 - (level-1)/10*0.5
                
        
        # Detect collitions
        if snake.head.xcor() > 290 or snake.head.xcor() < -290 or snake.head.ycor() > 290 or snake.head.ycor() < -290 or snake.bit_itself():
            game_state = False
            scoreboard.game_over()
        
    
    # Terminate
    screen.exitonclick()

if __name__ == "__main__":
    main()