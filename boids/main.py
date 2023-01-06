import random

from p5 import core
from p5.boids.boid import Boid


def setup():
    print("Setup START---------")
    core.fps = 30

    core.WINDOW_SIZE = [800  , 800]

    core.memory("boids", [])
    core.memory("boidsNb",200)

    for i in range(0,core.memory("boidsNb")):
        core.memory("boids").append(Boid(random.randint(0,0)))



    print("Setup END-----------")


def reset():
    core.memory("boids", [])
    for i in range(0,core.memory("boidsNb")):
        core.memory("boids").append(Boid(random.randint(0,2)))


def run():
    core.cleanScreen()
    if core.getKeyPressList("r"):
        reset()

    for b in core.memory("boids"):
        if core.getMouseLeftClick():
           b.repultion(core.getMouseLeftClick())

        if core.getMouseRightClick():
           b.attraction(core.getMouseRightClick())

        b.flock(core.memory("boids"))
        b.update()
        b.show()
        b.edge(core.WINDOW_SIZE)

core.main(setup, run)
