from turtle import Screen, _Screen, Turtle
from main_menu import MainMenu
from snake import Snake
from food import Food
from scoreboard import Scoreboard
import time

class Game():
    def __init__(self) -> None:
        self.screen = Screen()
        self.initial_level = 5
        self.running = False
        self.scoreboard = None
        
        # Create Screen
        self.screen.setup(width=600, height = 600)
        self.screen.title("Snake")
        
        # Run the game.
        self.game_menu()

               
    def game_menu(self):
        self.clear_screen()
        main_menu = MainMenu()
        
        # Listeners
        self.screen.onkey(fun=main_menu.go_up, key="Up")
        self.screen.onkey(fun=main_menu.go_down, key="Down")
        self.screen.onkey(fun=main_menu.increase_level, key="Right")
        self.screen.onkey(fun=main_menu.decrease_level, key="Left")
        self.screen.onkey(fun=self.break_loop, key="Return")
        
        self.screen.listen()
        
        self.running = True
        while self.running or main_menu.option == 2:
            main_menu.update_markers()
            self.screen.update()
            time.sleep(0.1)
            
        if main_menu.option == 1:
            self.initial_level = main_menu.level
            self.start_game()
            
        elif main_menu.option == 3:
            self.screen.bye()
                
    def break_loop(self):
        self.running = False
    
    def start_game(self,snake=None,food=None):         
        # Initialize Game   
        self.running = True
        self.clear_screen()
        
        snake = Snake()
        food = Food()
        self.scoreboard = Scoreboard()
        self.screen.update()
        
        # Listeners
        self.screen.onkeypress(fun=snake.set_orientation_up,key="Up")
        self.screen.onkeypress(fun=snake.set_orientation_right,key="Right")
        self.screen.onkeypress(fun=snake.set_orientation_down,key="Down")
        self.screen.onkeypress(fun=snake.set_orientation_left,key="Left")
        
        self.screen.onkeypress(fun=self.end_game,key="Escape")
        self.screen.onkeypress(fun=None,key="Return")

        self.screen.listen()
        
        # Game
        level = self.initial_level
        interval = 0.5 - (level-1)/10*0.5
        food_count = 0
        while self.running:
            self.screen.update()
            time.sleep(interval)
            snake.move_forward()
            # print(snake.snake_segments[0].pos())
            
            # Eating food
            if snake.head.distance(food) < 1:
                food.refresh_position()
                self.scoreboard.add_points(level)
                snake.extend()
                food_count += 1
                if food_count == 5 and level < 10:
                    food_count = 0
                    level += 1
                    interval = 0.5 - (level-1)/10*0.5
                    
            # Detect collitions
            if snake.bit_itself():
                self.end_game()
        
        
        # Wait for pressing enter to enter the main menu
        self.screen.onkeypress(fun=self.break_loop,key="Return")
        self.screen.onkeypress(fun=self.break_loop,key="Escape")

        self.running = True
        while self.running:
            time.sleep(0.5)
            self.screen.update()
        self.game_menu()
        
    def end_game(self):
        """End the game and show the 'Game Over' window."""
        self.running = False
        self.scoreboard.game_over()
            

    def turn_off_listeners(self):
        """Turns off the listeners"""
        self.screen.onkeypress(fun=None,key="Up")
        self.screen.onkeypress(fun=None,key="Right")
        self.screen.onkeypress(fun=None,key="Down")
        self.screen.onkeypress(fun=None,key="Left")
    
        self.screen.onkeypress(fun=None,key="Escape")

    def clear_screen(self):
        self.screen.clearscreen()
        self.screen.bgcolor("black")
        self.screen.tracer(0)

def main():   
    # Run the 
    game = Game()
    
    # Terminate
    game.screen.exitonclick()

if __name__ == "__main__":
    main()