from turtle import Turtle
FONT_LEVEL = ("Courier", 24, "normal")


class Scoreboard(Turtle):
    def __init__(self, shape: str = "classic", undobuffersize: int = 1000, visible: bool = True) -> None:
        super().__init__(shape, undobuffersize, visible)
        self.__level = 1
        
        self.hideturtle()
        self.penup()
        self.__print_level()
        
    
    def increase_level(self):
        """Increase current level by one"""
        self.__level += 1
        self.__update_level()

    def __print_level(self):
        self.goto(-280,260)
        self.write(f"Level: {self.__level}",align="left",font=FONT_LEVEL)
        
    def __update_level(self):
        self.clear()
        self.__print_level()
          
    def game_over(self):
        """Print the game over screen"""
        self.goto(0,-40)
        self.write("GAME OVER", align="center",font=("Arial",52,"bold"))