from turtle import Turtle

class Scoreboard(Turtle):
    def __init__(self, shape: str = "classic", undobuffersize: int = 1000, visible: bool = True) -> None:
        super().__init__(shape, undobuffersize, visible)
        self.score_player_1 = 0
        self.score_player_2 = 0
        
        self.hideturtle()
        self.penup()
        self.color("white")
        self.update()
        
    def update(self):
        self.clear()
        self.goto(-100,200)
        self.write(self.score_player_2, align="center", font= ("Courier", 80, "normal"))
        self.goto(100,200)
        self.write(self.score_player_1, align="center", font= ("Courier", 80, "normal"))
        
    def add_point_player1(self):
        self.score_player_1 += 1
        self.update()
        
    def add_point_player2(self):
        self.score_player_2 += 1
        self.update()