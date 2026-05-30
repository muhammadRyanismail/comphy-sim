import pygame
import math

class Body:

    def __init__(self,x,y,vx,vy,mass,color,fixed=False):

        self.x = x
        self.y = y

        self.vx = vx
        self.vy = vy

        self.mass = mass
        self.color = color

        self.fixed = fixed

        self.radius = max(2,int(math.sqrt(mass)))

        self.trail = []

    def draw(self,screen,trails):

        if trails and len(self.trail) > 2:

            pygame.draw.lines(
                screen,
                self.color,
                False,
                self.trail,
                1
            )

        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x),int(self.y)),
            self.radius
        )