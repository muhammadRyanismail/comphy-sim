import pygame
import random
import math

pygame.init()

WIDTH = 1600
HEIGHT = 900

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT)
)

pygame.display.set_caption(
    "Cosmic Sandbox Ultimate"
)

clock = pygame.time.Clock()

G = 0.05
TIME_SCALE = 1

BLACK = (0,0,0)
WHITE = (255,255,255)

STAR_COLORS = [
    (255,255,255),
    (120,180,255),
    (180,100,255),
    (255,220,120),
    (255,120,120)
]

PLANET_COLORS = [
    (120,255,120),
    (120,180,255),
    (255,180,120),
    (255,120,120),
    (220,220,220)
]

MODE = "GALAXY"

TRAILS = True
DRAW_LINES = False

font = pygame.font.SysFont(
    "Arial",
    20
)

formation_particles = []

class Body:

    def __init__(
        self,
        x,
        y,
        vx,
        vy,
        mass,
        color,
        fixed=False
    ):

        self.x = x
        self.y = y

        self.vx = vx
        self.vy = vy

        self.mass = mass

        self.color = color

        self.fixed = fixed

        self.radius = max(
            2,
            int(math.sqrt(mass))
        )

        self.trail = []

    def update(self,bodies):

        if self.fixed:
            return

        ax = 0
        ay = 0

        for other in bodies:

            if other == self:
                continue

            dx = other.x - self.x
            dy = other.y - self.y

            dist_sq = dx*dx + dy*dy + 25

            if dist_sq < 4:
                continue

            dist = math.sqrt(dist_sq)

            force = (
                G *
                self.mass *
                other.mass /
                dist_sq
            )

            ax += (
                force *
                dx /
                dist /
                self.mass
            )

            ay += (
                force *
                dy /
                dist /
                self.mass
            )

        self.vx += ax * TIME_SCALE
        self.vy += ay * TIME_SCALE

        self.x += self.vx * TIME_SCALE
        self.y += self.vy * TIME_SCALE

        if TRAILS:

            self.trail.append(
                (self.x,self.y)
            )

            if len(self.trail) > 30:
                self.trail.pop(0)

    def draw(self):

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
            (int(self.x),int(self.y)),
            self.radius
        )


class DemoStar:

    def __init__(
        self,
        x,
        y,
        vx,
        vy,
        color,
        size=2
    ):

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

        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x),int(self.y)),
            self.size
        )
        # =====================================
# GALAXY SANDBOX OBJECTS
# =====================================

def spawn_blackhole(x,y):

    bh = Body(
        x,
        y,
        0,
        0,
        50000,
        WHITE
    )

    bh.radius = 10

    return bh


def spawn_sun(x,y):

    sun = Body(
        x,
        y,
        0,
        0,
        12000,
        (255,220,120),
        True
    )

    sun.radius = 12

    return sun


def spawn_planet(x,y):

    return Body(
        x,
        y,
        random.uniform(-2,2),
        random.uniform(-2,2),
        12,
        random.choice(
            PLANET_COLORS
        )
    )


def spawn_galaxy(cx,cy):

    new_bodies = []

    core = Body(
        cx,
        cy,
        0,
        0,
        25000,
        WHITE
    )

    core.radius = 8

    new_bodies.append(core)

    for _ in range(350):

        angle = random.uniform(
            0,
            math.pi*2
        )

        distance = random.uniform(
            30,
            400
        )

        x = cx + math.cos(angle)*distance
        y = cy + math.sin(angle)*distance

        speed = math.sqrt(
            G * core.mass /
            (distance+1)
        )

        vx = -math.sin(angle)*speed
        vy = math.cos(angle)*speed

        vx += random.uniform(
            -0.5,
            0.5
        )

        vy += random.uniform(
            -0.5,
            0.5
        )

        star = Body(
            x,
            y,
            vx,
            vy,
            random.uniform(1,4),
            random.choice(
                STAR_COLORS
            )
        )

        new_bodies.append(star)

    return new_bodies


# =====================================
# FORMATION DEMOS
# =====================================

def create_gas_cloud(cx,cy):

    formation_particles.clear()

    for _ in range(1500):

        angle = random.uniform(
            0,
            math.tau
        )

        radius = random.uniform(
            0,
            300
        )

        x = cx + math.cos(angle)*radius
        y = cy + math.sin(angle)*radius

        vx = -(x-cx)*0.001
        vy = -(y-cy)*0.001

        formation_particles.append(

            DemoStar(
                x,
                y,
                vx,
                vy,
                (255,255,255)
            )

        )


def create_spiral(cx,cy):

    formation_particles.clear()

    for _ in range(2000):

        angle = random.uniform(
            0,
            math.tau*4
        )

        radius = random.uniform(
            20,
            320
        )

        spiral_angle = (
            angle +
            radius * 0.03
        )

        x = (
            cx +
            math.cos(
                spiral_angle
            ) *
            radius
        )

        y = (
            cy +
            math.sin(
                spiral_angle
            ) *
            radius
        )

        speed = (
            0.5 /
            max(radius/50,1)
        )

        vx = (
            -math.sin(
                spiral_angle
            ) *
            speed
        )

        vy = (
            math.cos(
                spiral_angle
            ) *
            speed
        )

        formation_particles.append(

            DemoStar(
                x,
                y,
                vx,
                vy,
                (200,220,255)
            )

        )


def create_merger():

    formation_particles.clear()

    left_x = WIDTH * 0.3
    right_x = WIDTH * 0.7

    cy = HEIGHT // 2

    for _ in range(1000):

        angle = random.uniform(
            0,
            math.tau
        )

        radius = random.uniform(
            20,
            150
        )

        x = (
            left_x +
            math.cos(angle)*radius
        )

        y = (
            cy +
            math.sin(angle)*radius
        )

        formation_particles.append(

            DemoStar(
                x,
                y,
                0.4,
                0,
                (255,220,150)
            )

        )

    for _ in range(1000):

        angle = random.uniform(
            0,
            math.tau
        )

        radius = random.uniform(
            20,
            150
        )

        x = (
            right_x +
            math.cos(angle)*radius
        )

        y = (
            cy +
            math.sin(angle)*radius
        )

        formation_particles.append(

            DemoStar(
                x,
                y,
                -0.4,
                0,
                (150,220,255)
            )

        )


def create_random_universe():

    formation_particles.clear()

    for _ in range(2500):

        formation_particles.append(

            DemoStar(

                random.randint(
                    0,
                    WIDTH
                ),

                random.randint(
                    0,
                    HEIGHT
                ),

                random.uniform(
                    -0.2,
                    0.2
                ),

                random.uniform(
                    -0.2,
                    0.2
                ),

                (255,255,255)

            )

        )
        # =====================================
# START
# =====================================

bodies = []

paused = False

running = True

# =====================================
# MAIN LOOP
# =====================================

while running:

    clock.tick(60)

    # =========================
    # EVENTS
    # =========================
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # SANDBOX TOOLS

            if event.key == pygame.K_1:
                MODE = "GALAXY"

            elif event.key == pygame.K_2:
                MODE = "BLACKHOLE"

            elif event.key == pygame.K_3:
                MODE = "PLANET"

            elif event.key == pygame.K_4:
                MODE = "SUN"

            # FORMATION DEMOS

            elif event.key == pygame.K_5:

                MODE = "GAS CLOUD"

                create_gas_cloud(
                    WIDTH//2,
                    HEIGHT//2
                )

            elif event.key == pygame.K_6:

                MODE = "SPIRAL"

                create_spiral(
                    WIDTH//2,
                    HEIGHT//2
                )

            elif event.key == pygame.K_7:

                MODE = "MERGER"

                create_merger()

            elif event.key == pygame.K_8:

                MODE = "RANDOM"

                create_random_universe()

            # OTHER

            elif event.key == pygame.K_SPACE:
                paused = not paused

            elif event.key == pygame.K_r:

                bodies.clear()
                formation_particles.clear()

            elif event.key == pygame.K_t:
                TRAILS = not TRAILS

            elif event.key == pygame.K_g:
                DRAW_LINES = not DRAW_LINES

        # LEFT CLICK

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                mx, my = pygame.mouse.get_pos()

                if MODE == "GALAXY":

                    bodies.extend(
                        spawn_galaxy(
                            mx,
                            my
                        )
                    )

                elif MODE == "BLACKHOLE":

                    bodies.append(
                        spawn_blackhole(
                            mx,
                            my
                        )
                    )

                elif MODE == "PLANET":

                    bodies.append(
                        spawn_planet(
                            mx,
                            my
                        )
                    )

                elif MODE == "SUN":

                    bodies.append(
                        spawn_sun(
                            mx,
                            my
                        )
                    )

    # =========================
    # BACKGROUND
    # =========================

    fade = pygame.Surface(
        (WIDTH, HEIGHT)
    )

    fade.set_alpha(30)

    fade.fill(BLACK)

    screen.blit(
        fade,
        (0,0)
    )

    # =========================
    # UPDATE
    # =========================

    if not paused:

        for body in bodies:
            body.update(
                bodies
            )

        for particle in formation_particles:
            particle.update()

    # =========================
    # GRAVITY WEB
    # =========================

    if DRAW_LINES:

        for i in range(
            0,
            len(bodies),
            12
        ):

            for j in range(
                i+1,
                min(
                    i+8,
                    len(bodies)
                )
            ):

                b1 = bodies[i]
                b2 = bodies[j]

                dx = b1.x - b2.x
                dy = b1.y - b2.y

                dist = math.sqrt(
                    dx*dx +
                    dy*dy
                )

                if dist < 120:

                    pygame.draw.line(
                        screen,
                        (80,60,140),
                        (
                            b1.x,
                            b1.y
                        ),
                        (
                            b2.x,
                            b2.y
                        ),
                        1
                    )

    # =========================
    # DRAW
    # =========================

    for body in bodies:
        body.draw()

    for particle in formation_particles:
        particle.draw()

    # =========================
    # HUD
    # =========================

    hud = [

        f"FPS: {int(clock.get_fps())}",
        f"Bodies: {len(bodies)}",
        f"Particles: {len(formation_particles)}",
        f"Mode: {MODE}",
        "",

        "1 = Galaxy",
        "2 = Black Hole",
        "3 = Planet",
        "4 = Sun",

        "",

        "5 = Gas Cloud",
        "6 = Spiral Galaxy",
        "7 = Galaxy Merger",
        "8 = Random Universe",

        "",

        "Left Click = Spawn",
        "SPACE = Pause",
        "R = Reset",
        "T = Trails",
        "G = Gravity Web"

    ]

    y = 10

    for line in hud:

        txt = font.render(
            line,
            True,
            WHITE
        )

        screen.blit(
            txt,
            (10,y)
        )

        y += 22

    # =========================
    # START MESSAGE
    # =========================

    if (
        len(bodies) == 0 and
        len(formation_particles) == 0
    ):

        bigfont = pygame.font.SysFont(
            "Arial",
            42
        )

        txt = bigfont.render(
            "CREATE YOUR UNIVERSE",
            True,
            (180,100,255)
        )

        screen.blit(
            txt,
            (
                WIDTH//2 -
                txt.get_width()//2,

                HEIGHT//2 -
                txt.get_height()//2
            )
        )

    pygame.display.flip()

pygame.quit()