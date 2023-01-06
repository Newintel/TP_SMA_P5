import random
import time

from pygame import Vector2, Color

from p5.sma.Fustrum import Fustrum
from p5 import core
from p5.sma.agent import Status
from p5.sma.epidemie import epidemie


class Stats:
    def __init__(self):
        self.incubation = -1
        self.contaminated = -1
        self.dying = -1

    def activate_incubation(self):
        if not self.is_incubation():
            self.incubation = time.time()

    def deactivate_incubation(self):
        self.incubation = -1

    def activate_contaminated(self):
        if not self.is_contaminated():
            self.contaminated = time.time()

    def deactivate_contaminated(self):
        self.contaminated = -1

    def activate_dying(self):
        if not self.is_dying():
            self.dying = time.time()

    def deactivate_dying(self):
        self.dying = -1

    def is_incubation(self):
        return self.incubation != -1

    def is_contaminated(self):
        return self.contaminated != -1

    def is_dying(self):
        return self.dying != -1


class Body:
    def __init__(self, pos: Vector2, radius: int):
        self.uuid = random.randbytes(10)  # TODO: generate uuid
        self.location = pos
        self.velocity = Vector2(0, 0)
        self.fustrum = Fustrum()
        self.radius = radius
        self.stats = Stats()

    def inside_perception(self, p):
        return self.fustrum.inside(self.location, p)

    def update(self) -> Status | None:
        if self.stats.is_incubation():
            if time.time() - self.stats.incubation > epidemie.get("incubation") * 1000:
                self.stats.deactivate_incubation()
                self.stats.activate_dying()
                return Status.Infected
        if self.stats.is_contaminated():
            if time.time() - self.stats.contaminated > epidemie.get("avant_contagion") * 1000 \
                    and random.randint(0, 100) < epidemie.get("contagion_pourcentage"):
                self.stats.deactivate_contaminated()
                self.stats.activate_incubation()
                return Status.Infected
        if self.stats.is_dying():
            if time.time() - self.stats.dying > epidemie.get("avant_deces") * 1000:
                if random.randint(0, 100) < epidemie.get("mortalite"):
                    self.stats.deactivate_dying()
                    return Status.Dead
                else:
                    self.stats.deactivate_dying()
                    return Status.Recovered
        return None

    def move(self):
        self.location += self.velocity.normalize()

    def show(self, color: Color):
        core.Draw.circle(color, self.location, self.radius)
