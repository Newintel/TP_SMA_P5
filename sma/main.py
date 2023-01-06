import random
from enum import Enum

from pygame.math import Vector2
from p5 import core
from p5.sma.agent import Agent, Status
from p5.sma.body import Body
from p5.sma.epidemie import epidemie
from p5.sma.item import Item


class Environment:
    def __init__(self):
        self.agents: list[Agent] = []
        self.items: list[Item] = []
        self.boardW = 400
        self.boardH = 400

    def add_agent(self, agent: Agent):
        self.agents.append(agent)

    def add_random_agent(self):
        x = random.uniform(0, self.boardW)
        y = random.uniform(0, self.boardH)
        self.add_agent(Agent(Vector2(x, y), 10))

    def compute_perception(self, agent: Agent):
        for other in self.agents:
            if agent.uuid != other.uuid:
                if agent.body.inside_perception(other.body.location):
                    agent.body.fustrum.perceptionList.append(other)

    def compute_decision(self, agent: Agent):
        for other in agent.body.fustrum.perceptionList:
            if agent.touches(other):
                agent.body.velocity = agent.body.location - other.body.location
            if other.status == Status.Infected \
                    and agent.body.location.distance_to(other) < epidemie.get("distance_min_contamination"):
                agent.body.stats.activate_contaminated()

        self.on_edges(agent.body)

    def apply_decision(self, agent: Agent):
        agent.body.move()
        agent.status = agent.body.update()

    def on_edges(self, b: Body):
        if b.location.x > self.boardW or b.location.x < 0:
            b.velocity.x *= -1

        if b.location.y > self.boardH or b.location.y < 0:
            b.velocity.y *= -1


def setup():
    print("Setup START---------")
    core.fps = 70
    env = Environment()

    for _ in range(20):
        env.add_random_agent()

    core.WINDOW_SIZE = [env.boardW, env.boardH]

    core.memory("env", env)

    print("Setup END-----------")


def computePerception(agent: Agent):
    env: Environment = core.memory("env")
    env.compute_perception(agent)


def computeDecision(agent: Agent):
    env: Environment = core.memory("env")
    env.compute_decision(agent)


def applyDecision(agent: Agent):
    env: Environment = core.memory("env")
    env.apply_decision(agent)


def run():
    core.cleanScreen()
    env: Environment = core.memory("env")

    # Display
    for agent in env.agents:
        agent.show()

    for item in env.items:
        item.show()

    for agent in env.agents:
        computePerception(agent)

    for agent in env.agents:
        computeDecision(agent)

    for agent in env.agents:
        applyDecision(agent)


core.main(setup, run)
