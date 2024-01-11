from turtle import Turtle


class MainMenu():
    def __init__(self) -> None:
        self.option = 1
        self.level = 1
        self.draw_title()
        self.options_turtle=[]
        self.draw_options()
        self.markers=[]
        self.create_markers()
    
    def draw_title(self):
        game_title = Turtle()
        game_title.hideturtle()
        game_title.penup()
        game_title.color("white")
        game_title.sety(150)
        game_title.write(arg="Snake",align="center",font=("OCR A Extended",100,"bold"))
        
    def draw_options(self):
        global OPTIONS_TEXT
        self.options_turtle = Turtle()
        self.options_turtle.hideturtle()
        self.options_turtle.penup()
        self.options_turtle.color("white")
        self.update_options()
            
    def update_options(self):
        self.options_turtle.clear()
        
        options_text = ["New Game", f"Level: < {self.level} >", "Quit Game"]

        for i in range(len(options_text)):
            self.options_turtle.sety(0-i*100)
            self.options_turtle.write(arg=options_text[i],align="center",font=("arial",26,"bold"))
            
    
    def create_markers(self):
        for i in range(3):
            marker = Turtle(shape="circle")
            marker.hideturtle()
            marker.penup()
            marker.color("white")
            marker.sety(20-i*100)
            marker.setx(-150)
            self.markers.append(marker)
    
    def update_markers(self):
        for i in range(len(self.markers)):
            if i == self.option-1:
                self.markers[i].showturtle()
            else:
                self.markers[i].hideturtle()
        self.update_options()

    def go_up(self):
        if self.option > 1:
            self.option -= 1
            
    def go_down(self):
        if self.option < 3:
            self.option += 1
            
    def increase_level(self):
        if self.option == 2 and self.level < 10:
            self.level +=1

    def decrease_level(self):
        if self.option == 2 and self.level > 1:
            self.level -=1