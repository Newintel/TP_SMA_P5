import random
from pygame.math import Vector2

from p5 import core

colorFamily=[(255,0,0),(0,255,0),(0,0,255)]
class Boid:
    def __init__(self,family=0):
        self.debug = False
        self.pos = Vector2(random.randint(0,800),random.randint(0,800))
        self.vel = Vector2(random.uniform(-5,5),random.uniform(-5,5))
        self.acc = Vector2()
        self.family = family
        self.maxAcc=1
        self.maxSpeed=4
        self.perception = 100
        self.separationFactor=1
        self.alignFactor = 0.1
        self.cohesionFactor = 1
        self.se=Vector2()
        self.co = Vector2()



    def update(self):
        if self.acc.length() > self.maxAcc:
            self.acc.scale_to_length(self.maxAcc)

        self.vel+=self.acc
        if self.vel.length() > self.maxSpeed:
            self.vel.scale_to_length(self.maxSpeed)
        self.acc=Vector2(0,0)
        self.pos+=self.vel



    def flock(self,boids):
        boidsPerception=[]
        for b in boids:
            if self.pos.distance_to(b.pos) < self.perception :
                if b.family == self.family:
                    if self != b:
                        boidsPerception.append(b)

        self.co = self.cohesion(boidsPerception)*self.cohesionFactor
        al = self.align(boidsPerception)*self.alignFactor
        self.se = self.separation(boidsPerception)*-self.separationFactor


        self.acc+= self.se + self.co + al


    def repultion(self,obstacle):
        obstacleVect = Vector2(obstacle[0], obstacle[1])
        if obstacleVect.distance_to(self.pos) < self.perception*2:
            self.acc =   self.pos - obstacleVect

    def attraction(self,obstacle):
        obstacleVect = Vector2(obstacle[0], obstacle[1])
        if obstacleVect.distance_to(self.pos) < self.perception*2:
            self.acc =   obstacleVect  - self.pos




    def separation(self,boids):
        steering = Vector2()
        boidscounter = 0
        for other in boids:
            if self.pos.distance_to(other.pos) != 0:
                diff = Vector2(other.pos.x-self.pos.x,other.pos.y-self.pos.y)
                if diff.length() > 0.001:
                    diff.scale_to_length(self.pos.distance_squared_to(other.pos))
                    boidscounter += 1
                    steering += diff
            else:
                steering += Vector2(random.uniform(-5,5),random.uniform(-5,5))
                boidscounter += 1

        if boidscounter > 0:
            steering /= boidscounter

            steering += self.vel

            if steering.length() > self.maxAcc:
                steering = steering.normalize()
                steering.scale_to_length(self.maxAcc)
        return steering

    def cohesion(self,boids):
        steering = Vector2()
        boidscounter = 0
        for other in boids:
            if self.pos.distance_to(other.pos) != 0:
                boidscounter += 1
                steering += other.pos

        if boidscounter > 0:
            steering /= boidscounter
            steering -= self.pos


            steering += self.vel
            if steering.length() > self.maxAcc:
                steering = steering.normalize()
                steering.scale_to_length(self.maxAcc)

        return steering

    def align(self,boids):
        steering = Vector2()
        boidscounter = 0
        for other in boids:
            boidscounter+=1
            steering+=other.vel

        if boidscounter>0:
            steering/=boidscounter

            steering -= self.vel
            if steering.length() > self.maxAcc:
                steering=steering.normalize()
                steering.scale_to_length(self.maxAcc)

        return steering

    def edge(self,sizes):
        if self.pos.x <0:
            self.pos.x = sizes[0]
        if self.pos.x > sizes[0]:
            self.pos.x = 0
        if self.pos.y <0:
            self.pos.y = sizes[1]
        if self.pos.y > sizes[1]:
            self.pos.y = 0

    def show(self):
        a = 0 - self.vel.angle_to(Vector2(0,1))


        p1 = self.pos + Vector2(-5, 0).rotate(a)
        p2 = self.pos + Vector2(0, 15).rotate(a)
        p3 = self.pos + Vector2(5, 0).rotate(a)

        core.Draw.polygon(colorFamily[self.family], ((p1), (p2), (p3)))

        if self.debug:
            core.Draw.line((255,255,255),self.pos,self.pos+self.co*50)
            core.Draw.line((255, 0, 0), self.pos, self.pos + self.se * 50)
            #pygame.draw.circle(screen,(255,255,255),self.pos,self.perception,1)
