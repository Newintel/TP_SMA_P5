import random
from enum import Enum
from typing import Self

from pygame import Vector2, Color

from p5.sma.body import Body


class Status(Enum):
    Sane = 0
    Infected = 1
    Recovered = 2
    Dead = 3


class Agent:
    def __init__(self, pos: Vector2, radius: int):
        self.uuid = random.randbytes(10)  # TODO: generate a unique id
        self.body = Body(pos, radius)
        self.status = Status.Sane
        self.move_random()

    def move_random(self):
        x = int(random.uniform(-10, 10))
        y = int(random.uniform(-10, 10))
        self.body.velocity = Vector2(x, y).normalize()

    def get_color(self) -> Color:
        if self.status == Status.Sane:
            return Color("green")
        elif self.status == Status.Infected:
            return Color("red")
        else:
            return Color("blue")

    def touches(self, other: Self) -> bool:
        return self.body.location.distance_to(other.body.location) <= self.body.radius

    def show(self):
        self.body.show(self.get_color())
