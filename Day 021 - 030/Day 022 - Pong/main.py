from turtle import Screen
from paddle import Paddle
from ball import Ball
from scoreboard import Scoreboard
import time

# Setup the screen
screen = Screen()
    
screen.setup(width=800, height=600)
screen.title("Pong")

def clear_screen():
    screen.clearscreen()
    screen.bgcolor("black")
    screen.tracer(0)
clear_screen()
screen.onkeypress(fun=screen.bye, key="Escape")

# Create the paddles
player_1 = Paddle((350,0))
screen.onkeypress(fun=player_1.move_up, key="Up")
screen.onkeypress(fun=player_1.move_down, key="Down")

player_2 = Paddle((-350,0))
screen.onkeypress(fun=player_2.move_up, key="w")
screen.onkeypress(fun=player_2.move_down, key="s")

ball = Ball()
scoreboard = Scoreboard()
screen.listen()


game_running = True
while game_running:
    screen.update()
    time.sleep(0.03)
    ball.move()
    if ball.hit_top_wall() or ball.hit_bottom_wall():
        ball.bounce_from_wall()
        
    if ball.hit_paddle(player_1) or ball.hit_paddle(player_2):
        ball.bounce_from_paddle()
        
    if ball.xcor() > 450:
        ball.reset_position()
        scoreboard.add_point_player2()
    elif ball.xcor() < -450:
        ball.reset_position()
        scoreboard.add_point_player1()

screen.mainloop()
