from turtle import Turtle
from player import Player
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_X = 320
STARTING_MOVE_DISTANCE = 3
MOVE_INCREMENT = 1
NUMBER_OF_CARS = 30


class CarManager:
    def __init__(self):
        self.cars = []
        self.car_speed = STARTING_MOVE_DISTANCE
        for _ in range(NUMBER_OF_CARS):
            self.__create_a_car()
            
    def __create_a_car(self):
        car = Car()
        if car.collides_with_other_cars(self.cars):
            self.__create_a_car()
        else:
            self.cars.append(car)
               
    def move_cars(self):
        for car in self.cars:
            car.forward(self.car_speed)
            if car.reached_finish_line():
                car.reset_car()
                while car.collides_with_other_cars(self.cars):
                    car.reset_car()
                
    def shuffle_cars(self):
        for _ in range(STARTING_MOVE_DISTANCE*100):
            self.move_cars() 
                
    def increase_speed(self):
        self.car_speed += MOVE_INCREMENT
        
    def hit_turtle(self,player):
        for car in self.cars:
            if abs(car.xcor()-player.xcor()) < 25 and abs(car.ycor()-player.ycor()) < 20:
                return True
        else:
            return False
            
class Car(Turtle):
    def __init__(self, shape: str = "square", undobuffersize: int = 1000, visible: bool = True) -> None:
        super().__init__(shape, undobuffersize, visible)
        self.shapesize(stretch_len=2)
        self.penup()
        self.color(random.choice(COLORS))
        self.reset_car()
        
    def reached_finish_line(self):
        return abs(self.xcor()) > 320 
    
    def collides_with_other_cars(self,cars):
        for car in cars:
            if self is car:
                continue
            if abs(car.xcor() - self.xcor()) < 40 and abs(car.ycor() - self.ycor()) < 25:
                return True
        else:
            return False
        
    def reset_car(self):
        ycor = random.randint(10,250)
        ycor *= random.choice([-1,1]) # randomly choose a side.
        xcor = random.randint(320,620)

        if ycor > 0:
            self.finish_line = -320
            self.goto(xcor,ycor)
            self.setheading(180)
        else:
            xcor *=-1
            self.finish_line = 320
            self.goto(xcor,ycor)
            self.setheading(0)