from turtle import Turtle

class Map(Turtle):
    def __init__(self, shape: str = "classic", undobuffersize: int = 1000, visible: bool = True) -> None:
        super().__init__(shape, undobuffersize, visible)
        self.hideturtle()
        self.penup()
        self.__print_road()
        
    def __print_road(self):
        """Print the map."""
        # Bottom line
        self.goto((-320,-260))
        self.pendown()
        self.goto((320,-260))
        self.penup()
        # Middle line
        self.goto((320,0))
        self.pendown()
        self.goto((-320,0))
        self.penup()
        # Top line
        self.goto((-320,260))
        self.pendown()
        self.goto((320,260))
        self.penup()