import random
import math

from body import Body
from settings import *

def spawn_blackhole(x,y):

    obj = Body(
        x,y,
        0,0,
        50000,
        WHITE
    )

    obj.radius = 10

    return obj

def spawn_sun(x,y):

    obj = Body(
        x,y,
        0,0,
        12000,
        (255,220,120),
        True
    )

    obj.radius = 12

    return obj

def spawn_planet(x,y):

    return Body(
        x,y,
        random.uniform(-2,2),
        random.uniform(-2,2),
        12,
        random.choice(PLANET_COLORS)
    )

def spawn_galaxy(cx,cy):

    bodies = []

    core = Body(
        cx,cy,
        0,0,
        25000,
        WHITE
    )

    core.radius = 8

    bodies.append(core)

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

        star = Body(
            x,
            y,
            vx,
            vy,
            random.uniform(1,4),
            random.choice(STAR_COLORS)
        )

        bodies.append(star)

    return bodies