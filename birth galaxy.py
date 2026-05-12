import pygame
import random
import math

            
WIDTH = 1280
HEIGHT = 720

CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

G = 0.05
DT = 0.15
SOFTENING = 5
CORE_MASS = 18000

MAX_PARTICLES = 1200
SPAWN_RATE = 4

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaxy Formation Simulation")

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 22)


class Particle:

    def __init__(self):

        angle = random.uniform(0, math.pi * 2)
        radius = random.uniform(0, 80)

        self.x = CENTER_X + math.cos(angle) * radius
        self.y = CENTER_Y + math.sin(angle) * radius

        self.vx = random.uniform(-1.2, 1.2)
        self.vy = random.uniform(-1.2, 1.2)

    def update(self):

        dx = CENTER_X - self.x
        dy = CENTER_Y - self.y

        distance_sq = dx * dx + dy * dy + SOFTENING

        distance = math.sqrt(distance_sq)

        nx = dx / distance
        ny = dy / distance

    
        gravity = G * CORE_MASS / distance_sq

        ax = nx * gravity
        ay = ny * gravity

        tangent_x = -ny
        tangent_y = nx

        swirl_strength = 0.018

        ax += tangent_x * swirl_strength
        ay += tangent_y * swirl_strength

        self.vx += ax * DT
        self.vy += ay * DT


        self.x += self.vx * DT
        self.y += self.vy * DT

    def draw(self, surface):

        speed = math.sqrt(self.vx ** 2 + self.vy ** 2)

        brightness = min(255, int(100 + speed * 35))

        color = (brightness, brightness, 255)

        pygame.draw.circle(
            surface,
            color,
            (int(self.x), int(self.y)),
            2
        )


particles = []

trail_surface = pygame.Surface((WIDTH, HEIGHT))
trail_surface.set_alpha(18)
trail_surface.fill((0, 0, 0))

running = True


while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if len(particles) < MAX_PARTICLES:

        for _ in range(SPAWN_RATE):
            particles.append(Particle())

    screen.blit(trail_surface, (0, 0))

    pygame.draw.circle(
        screen,
        (180, 60, 255),
        (CENTER_X, CENTER_Y),
        12
    )

    pygame.draw.circle(
        screen,
        (255, 255, 255),
        (CENTER_X, CENTER_Y),
        4
    )

    for particle in particles:
        particle.update()
        particle.draw(screen)

    title = font.render(
        "Galaxy Formation Simulation",
        True,
        (255, 255, 255)
    )

    subtitle = font.render(
        "Empty Space -> Particles -> Spiral Galaxy",
        True,
        (180, 180, 180)
    )

    particle_text = font.render(
        f"Particles: {len(particles)}",
        True,
        (120, 200, 255)
    )

    screen.blit(title, (20, 20))
    screen.blit(subtitle, (20, 50))
    screen.blit(particle_text, (20, 80))

    pygame.display.flip()

pygame.quit()