import math
import pygame


class Body:
    def __init__(
        self,
        x,
        y,
        vx,
        vy,
        mass,
        color,
        radius=2,
        body_type="star",
        fixed=False,
    ):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.mass = float(mass)
        self.color = color
        self.radius = radius
        self.body_type = body_type
        self.fixed = fixed
        self.trail = []

    def add_trail(self, max_length=45):
        self.trail.append((self.x, self.y))
        if len(self.trail) > max_length:
            self.trail.pop(0)

    def draw(self, screen, trails=True):
        if trails and len(self.trail) > 2:
            pygame.draw.lines(
                screen,
                self.color,
                False,
                self.trail,
                1,
            )

        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x), int(self.y)),
            int(self.radius),
        )

        # Draw a ring around black holes so they look special without becoming huge.
        if self.body_type == "black_hole":
            pygame.draw.circle(
                screen,
                (120, 80, 255),
                (int(self.x), int(self.y)),
                int(self.radius + 5),
                1,
            )