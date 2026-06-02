import math
import pygame


class DemoParticle:
    def __init__(self, x, y, vx, vy, color, radius=2):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.color = color
        self.radius = radius
        self.trail = []

    def update_simple(self):
        self.x += self.vx
        self.y += self.vy

    def update_attracted_to_point(self, cx, cy, strength=0.08):
        dx = cx - self.x
        dy = cy - self.y
        dist_sq = dx * dx + dy * dy + 100
        dist = math.sqrt(dist_sq)

        self.vx += strength * dx / dist
        self.vy += strength * dy / dist

        self.x += self.vx
        self.y += self.vy

    def update_restricted(self, attractors, g=0.08, time_scale=1.0, damping=0.999):
        ax = 0.0
        ay = 0.0

        for core in attractors:
            dx = core.x - self.x
            dy = core.y - self.y

            dist_sq = dx * dx + dy * dy + 30000
            dist = math.sqrt(dist_sq)

            a = g * core.mass / dist_sq

            ax += a * dx / dist
            ay += a * dy / dist

        self.vx += ax * time_scale
        self.vy += ay * time_scale

        self.vx *= damping
        self.vy *= damping

        self.x += self.vx * time_scale
        self.y += self.vy * time_scale

    def draw(self, screen, trails=False):
        if trails:
            self.trail.append((self.x, self.y))
            if len(self.trail) > 20:
                self.trail.pop(0)

            if len(self.trail) > 2:
                pygame.draw.lines(screen, self.color, False, self.trail, 1)

        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x), int(self.y)),
            self.radius,
        )