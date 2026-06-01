import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaxy Formation Simulator")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)

particles = []


class Star:
    def __init__(self, x, y, vx, vy, color, size=2):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self):
        if 0 <= self.x <= WIDTH and 0 <= self.y <= HEIGHT:
            pygame.draw.circle(
                screen,
                self.color,
                (int(self.x), int(self.y)),
                self.size
            )


def create_gas_cloud():
    particles.clear()

    cx, cy = WIDTH // 2, HEIGHT // 2

    for _ in range(1500):
        angle = random.uniform(0, math.tau)
        radius = random.uniform(0, 300)

        x = cx + math.cos(angle) * radius
        y = cy + math.sin(angle) * radius

        vx = -(x - cx) * 0.001
        vy = -(y - cy) * 0.001

        particles.append(
            Star(x, y, vx, vy, (255, 255, 255))
        )


def create_spiral():
    particles.clear()

    cx, cy = WIDTH // 2, HEIGHT // 2

    for _ in range(2000):
        angle = random.uniform(0, math.tau * 4)
        radius = random.uniform(20, 320)

        spiral_angle = angle + radius * 0.03

        x = cx + math.cos(spiral_angle) * radius
        y = cy + math.sin(spiral_angle) * radius

        speed = 0.5 / max(radius / 50, 1)

        vx = -math.sin(spiral_angle) * speed
        vy = math.cos(spiral_angle) * speed

        particles.append(
            Star(x, y, vx, vy, (200, 220, 255))
        )


def create_merger():
    particles.clear()

    left_x = WIDTH * 0.3
    right_x = WIDTH * 0.7
    cy = HEIGHT // 2

    for _ in range(1000):
        angle = random.uniform(0, math.tau)
        radius = random.uniform(20, 150)

        x = left_x + math.cos(angle) * radius
        y = cy + math.sin(angle) * radius

        particles.append(
            Star(x, y, 0.4, 0, (255, 220, 150))
        )

    for _ in range(1000):
        angle = random.uniform(0, math.tau)
        radius = random.uniform(20, 150)

        x = right_x + math.cos(angle) * radius
        y = cy + math.sin(angle) * radius

        particles.append(
            Star(x, y, -0.4, 0, (150, 220, 255))
        )


def create_random_universe():
    particles.clear()

    for _ in range(2500):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)

        vx = random.uniform(-0.2, 0.2)
        vy = random.uniform(-0.2, 0.2)

        particles.append(
            Star(x, y, vx, vy, (255, 255, 255))
        )


create_gas_cloud()

running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                create_gas_cloud()

            if event.key == pygame.K_2:
                create_spiral()

            if event.key == pygame.K_3:
                create_merger()

            if event.key == pygame.K_4:
                create_random_universe()

    screen.fill((0, 0, 10))

    title = font.render(
        "1: Gas Cloud Collapse | 2: Spiral Galaxy | 3: Galaxy Merger | 4: Random Universe",
        True,
        (255, 255, 255)
    )

    screen.blit(title, (20, 20))

    for star in particles:
        star.update()
        star.draw()

    pygame.display.flip()

pygame.quit()