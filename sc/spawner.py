import random
import math

from matplotlib.pylab import angle

from body import Body
from visual import DemoParticle
from settings import *


def spawn_black_hole(x, y):
    return Body(
        x,
        y,
        0,
        0,
        mass=60000,
        color=WHITE,
        radius=8,
        body_type="black_hole",
    )


def spawn_galactic_core(x, y, vx=0, vy=0):
    return Body(
        x,
        y,
        vx,
        vy,
        mass=30000,
        color=(230, 230, 255),
        radius=7,
        body_type="galactic_core",
    )


def spawn_sun(x, y):
    return Body(
        x,
        y,
        random.uniform(-0.5, 0.5),
        random.uniform(-0.5, 0.5),
        mass=1200,
        color=YELLOW,
        radius=5,
        body_type="sun",
    )


def spawn_planet(x, y):
    return Body(
        x,
        y,
        random.uniform(-2, 2),
        random.uniform(-2, 2),
        mass=8,
        color=random.choice(PLANET_COLORS),
        radius=3,
        body_type="planet",
    )


def spawn_galaxy(cx, cy, core_vx=0, core_vy=0, star_count=260, radius=360):
    bodies = []

    core = spawn_galactic_core(cx, cy, core_vx, core_vy)
    bodies.append(core)

    for _ in range(star_count):
        angle = random.uniform(0, math.tau)
        distance = random.uniform(35, radius)

        x = cx + math.cos(angle) * distance
        y = cy + math.sin(angle) * distance

        speed = math.sqrt(G * core.mass / (distance + 1))

        vx = -math.sin(angle) * speed + core_vx
        vy = math.cos(angle) * speed + core_vy

        vx += random.uniform(-0.12, 0.12)
        vy += random.uniform(-0.12, 0.12)

        star = Body(
            x,
            y,
            vx,
            vy,
            mass=random.uniform(1.5, 4.0),
            color=random.choice(STAR_COLORS),
            radius=2,
            body_type="star",
        )

        bodies.append(star)

    return bodies


def spawn_rogue_star_cluster(cx, cy, target_x, target_y, count=45):
    bodies = []

    dx = target_x - cx
    dy = target_y - cy
    dist = math.sqrt(dx * dx + dy * dy) + 1

    base_vx = dx / dist * 0.75
    base_vy = dy / dist * 0.75

    for _ in range(count):
        angle = random.uniform(0, math.tau)
        distance = random.uniform(0, 55)

        x = cx + math.cos(angle) * distance
        y = cy + math.sin(angle) * distance

        vx = base_vx + random.uniform(-0.15, 0.15)
        vy = base_vy + random.uniform(-0.15, 0.15)

        bodies.append(
            Body(
                x,
                y,
                vx,
                vy,
                mass=random.uniform(1.5, 4.0),
                color=random.choice(STAR_COLORS),
                radius=2,
                body_type="star",
            )
        )

    return bodies


def spawn_new_starburst(cx, cy, count=65):
    bodies = []

    for _ in range(count):
        angle = random.uniform(0, math.tau)
        distance = random.uniform(80, 260)

        x = cx + math.cos(angle) * distance
        y = cy + math.sin(angle) * distance

        speed = 0.45

        vx = -math.sin(angle) * speed + random.uniform(-0.12, 0.12)
        vy = math.cos(angle) * speed + random.uniform(-0.12, 0.12)

        bodies.append(
            Body(
                x,
                y,
                vx,
                vy,
                mass=random.uniform(1.0, 3.0),
                color=random.choice(STAR_COLORS),
                radius=2,
                body_type="star",
            )
        )

    return bodies


def create_formation_cloud(cx, cy, count=350):
    bodies = []

    for _ in range(count):
        angle = random.uniform(0, math.tau)

        # sqrt(random) distributes points more evenly over area.
        distance = math.sqrt(random.random()) * 380

        x = cx + math.cos(angle) * distance
        y = cy + math.sin(angle) * distance

        # Small tangential velocity gives the cloud angular momentum,
        # so it can settle into a rotating galaxy-like structure.
        rotation = 0.0045
        vx = -math.sin(angle) * distance * rotation
        vy = math.cos(angle) * distance * rotation

        # Slight inward collapse
        vx += -math.cos(angle) * 0.15
        vy += -math.sin(angle) * 0.15

        # Small random noise only
        vx += random.uniform(-0.08, 0.08)
        vy += random.uniform(-0.08, 0.08)

        body = Body(
            x,
            y,
            vx,
            vy,
            mass=random.uniform(1.5, 5.0),
            color=random.choice(STAR_COLORS),
            radius=2,
            body_type="star",
        )

        bodies.append(body)

    # This is a "protogalactic dense region", not a black hole.
    seed = Body(
        cx + random.uniform(-20, 20),
        cy + random.uniform(-20, 20),
        0,
        0,
        mass=12000,
        color=(210, 210, 255),
        radius=5,
        body_type="proto_core",
    )

    bodies.append(seed)

    return bodies


def create_visual_gas_cloud(cx, cy, count=1500):
    particles = []

    for _ in range(count):
        angle = random.uniform(0, math.tau)
        distance = random.uniform(0, 330)

        x = cx + math.cos(angle) * distance
        y = cy + math.sin(angle) * distance

        vx = -(x - cx) * 0.001
        vy = -(y - cy) * 0.001

        particles.append(DemoParticle(x, y, vx, vy, WHITE, 2))

    return particles


def create_visual_spiral(cx, cy, count=1900):
    particles = []

    for _ in range(count):
        angle = random.uniform(0, math.tau * 4)
        distance = random.uniform(20, 330)

        spiral_angle = angle + distance * 0.03

        x = cx + math.cos(spiral_angle) * distance
        y = cy + math.sin(spiral_angle) * distance

        speed = 0.5 / max(distance / 50, 1)

        vx = -math.sin(spiral_angle) * speed
        vy = math.cos(spiral_angle) * speed

        particles.append(DemoParticle(x, y, vx, vy, (200, 220, 255), 2))

    return particles


def create_visual_random_universe(count=2300):
    particles = []

    for _ in range(count):
        particles.append(
            DemoParticle(
                random.randint(0, WIDTH),
                random.randint(0, HEIGHT),
                random.uniform(-0.2, 0.2),
                random.uniform(-0.2, 0.2),
                WHITE,
                2,
            )
        )

    return particles


def create_restricted_merger():
    cores = []
    particles = []

    left_x = WIDTH * 0.20
    right_x = WIDTH * 0.80

    left_y = HEIGHT * 0.42
    right_y = HEIGHT * 0.58

    left_core = Body(
        left_x,
        left_y,
        0.18,
        0.05,
        mass=28000,
        color=(255, 220, 150),
        radius=7,
        body_type="galaxy_core",
    )

    right_core = Body(
        right_x,
        right_y,
        -0.18,
        -0.05,
        mass=28000,
        color=(150, 220, 255),
        radius=7,
        body_type="galaxy_core",
    )

    cores.extend([left_core, right_core])

    # Left galaxy
    for _ in range(900):
        angle = random.uniform(0, math.tau)
        distance = random.uniform(80, 360)

        x = left_x + math.cos(angle) * distance
        y = left_y + math.sin(angle) * distance

        softening = 30000
        speed = math.sqrt(
            G * left_core.mass * distance * distance /
            ((distance * distance + softening) ** 1.5)
        ) * 1.15

        vx = -math.sin(angle) * speed + left_core.vx
        vy = math.cos(angle) * speed + left_core.vy

        vx += random.uniform(-0.04, 0.04)
        vy += random.uniform(-0.04, 0.04)

        particles.append(
            DemoParticle(x, y, vx, vy, (255, 220, 150), 2)
        )

    # Right galaxy
    for _ in range(900):
        angle = random.uniform(0, math.tau)
        distance = random.uniform(80, 360)

        x = right_x + math.cos(angle) * distance
        y = right_y + math.sin(angle) * distance

        softening = 30000
        speed = math.sqrt(
            G * right_core.mass * distance * distance /
            ((distance * distance + softening) ** 1.5)
        ) * 1.15

        # Opposite spin makes the collision easier to see visually
        vx = math.sin(angle) * speed + right_core.vx
        vy = -math.cos(angle) * speed + right_core.vy

        vx += random.uniform(-0.04, 0.04)
        vy += random.uniform(-0.04, 0.04)

        particles.append(
            DemoParticle(x, y, vx, vy, (150, 220, 255), 2)
        )

    return cores, particles