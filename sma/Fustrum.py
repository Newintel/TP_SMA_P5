from pygame import Vector2


class Fustrum:
    def __init__(self):
        self.perceptionList = []
        self.radius = 100

    def inside(self, p_body: Vector2, p_object: Vector2):
        return p_body.distance_to(p_object) < self.radius
