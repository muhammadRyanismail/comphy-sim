import pygame
import random
import math

pygame.init()


WIDTH, HEIGHT = 1400, 900

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("N-Body Galaxy Formation & Evolution")

clock = pygame.time.Clock()


NUM_STARS = 1200

G = 0.08
CENTER_MASS = 25000

TIME_SCALE = 1

STAR_MIN_MASS = 1
STAR_MAX_MASS = 4

TRAILS = True
DRAW_LINES = False


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (100, 180, 255)
PURPLE = (180, 100, 255)
YELLOW = (255, 230, 120)
RED = (255, 120, 120)

STAR_COLORS = [
    WHITE,
    BLUE,
    PURPLE,
    YELLOW,
    RED
]


class Body:

    def __init__(self, x, y, vx, vy, mass, color):

        self.x = x
        self.y = y

        self.vx = vx
        self.vy = vy

        self.mass = mass
        self.color = color

        self.radius = max(1, int(math.sqrt(mass)))

        self.trail = []

    def update(self, bodies):

        ax = 0
        ay = 0

        for other in bodies:

            if other == self:
                continue

            dx = other.x - self.x
            dy = other.y - self.y

            dist_sq = dx * dx + dy * dy + 0.01
            dist = math.sqrt(dist_sq)

            force = G * self.mass * other.mass / dist_sq

            ax += force * dx / dist / self.mass
            ay += force * dy / dist / self.mass

       
        self.vx += ax * TIME_SCALE
        self.vy += ay * TIME_SCALE

      
        self.x += self.vx * TIME_SCALE
        self.y += self.vy * TIME_SCALE

      
        if TRAILS:

            self.trail.append((self.x, self.y))

            if len(self.trail) > 25:
                self.trail.pop(0)

    def draw(self, screen):

        
        if TRAILS and len(self.trail) > 2:

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
            (int(self.x), int(self.y)),
            self.radius
        )


def create_galaxy():

    bodies = []

    
    center = Body(
        WIDTH // 2,
        HEIGHT // 2,
        0,
        0,
        CENTER_MASS,
        WHITE
    )

    center.radius = 8

    bodies.append(center)

    
    for i in range(NUM_STARS):

        angle = random.uniform(0, math.pi * 2)

       
        distance = max(40, abs(random.gauss(220, 90)))

        x = WIDTH // 2 + math.cos(angle) * distance
        y = HEIGHT // 2 + math.sin(angle) * distance

        
        speed = math.sqrt(G * CENTER_MASS / (distance + 1))

        vx = -math.sin(angle) * speed
        vy = math.cos(angle) * speed

       
        vx += random.uniform(-0.3, 0.3)
        vy += random.uniform(-0.3, 0.3)

        mass = random.uniform(
            STAR_MIN_MASS,
            STAR_MAX_MASS
        )

        color = random.choice(STAR_COLORS)

        star = Body(
            x,
            y,
            vx,
            vy,
            mass,
            color
        )

        bodies.append(star)

    return bodies


bodies = create_galaxy()

paused = False


running = True

while running:

    clock.tick(60)

    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

        
            if event.key == pygame.K_SPACE:
                paused = not paused

           
            if event.key == pygame.K_r:
                bodies = create_galaxy()

           
            if event.key == pygame.K_g:
                DRAW_LINES = not DRAW_LINES

            
            if event.key == pygame.K_t:
                TRAILS = not TRAILS

    
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                mx, my = pygame.mouse.get_pos()

                blackhole = Body(
                    mx,
                    my,
                    0,
                    0,
                    8000,
                    WHITE
                )

                blackhole.radius = 6

                bodies.append(blackhole)

  
    fade = pygame.Surface((WIDTH, HEIGHT))

    fade.set_alpha(35)

    fade.fill(BLACK)

    screen.blit(fade, (0, 0))

    
    if not paused:

        for body in bodies:
            body.update(bodies)

  
    if DRAW_LINES:

        for i in range(0, len(bodies), 15):

            for j in range(i + 1, min(i + 10, len(bodies))):

                b1 = bodies[i]
                b2 = bodies[j]

                dx = b1.x - b2.x
                dy = b1.y - b2.y

                dist = math.sqrt(dx * dx + dy * dy)

                if dist < 100:

                    color = (80, 60, 140)

                    pygame.draw.line(
                        screen,
                        color,
                        (b1.x, b1.y),
                        (b2.x, b2.y),
                        1
                    )


    for body in bodies:
        body.draw(screen)

    font = pygame.font.SysFont("Arial", 20)

    text = font.render(
        f"Bodies: {len(bodies)} | SPACE Pause | R Reset | G Gravity Web | T Trails | Click = Black Hole",
        True,
        WHITE
    )

    screen.blit(text, (15, 15))

    
    pygame.display.flip()

pygame.quit()