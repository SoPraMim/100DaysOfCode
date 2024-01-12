# Imports
import time
from turtle import Screen
from player import Player
from car_manager import CarManager
from scoreboard import Scoreboard
from map import Map

# Create the screen
screen = Screen()
screen.title("Turtle Crossing")
screen.setup(width=600, height=600)
screen.tracer(0)

# Create the game screen
map = Map()
scoreboard = Scoreboard()
car_manager = CarManager()
car_manager.shuffle_cars()

player = Player()
screen.onkeypress(fun=player.move_forward, key="Up")
screen.listen()


game_is_on = True
while game_is_on:
    time.sleep(0.03)
    screen.update()
    car_manager.move_cars()
    
    # Level up
    if player.reached_the_finish_line():
        player.reset_position()
        car_manager.increase_speed()
        scoreboard.increase_level()
        
    # Turtle got killed
    if car_manager.hit_turtle(player):
        screen.update()
        scoreboard.game_over()
        game_is_on = False
        
screen.mainloop()