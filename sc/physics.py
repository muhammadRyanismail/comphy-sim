import math
from settings import G, SOFTENING


def update_nbody(bodies, trails=True, time_scale=1.0):
    accelerations = []

    for body in bodies:
        ax = 0.0
        ay = 0.0

        if body.fixed:
            accelerations.append((0.0, 0.0))
            continue

        for other in bodies:
            if other is body:
                continue

            dx = other.x - body.x
            dy = other.y - body.y

            dist_sq = dx * dx + dy * dy + SOFTENING
            dist = math.sqrt(dist_sq)

            # Acceleration from Newtonian gravity:
            # a = G * M / r^2
            a = G * other.mass / dist_sq

            ax += a * dx / dist
            ay += a * dy / dist

        accelerations.append((ax, ay))

    for body, (ax, ay) in zip(bodies, accelerations):
        if body.fixed:
            continue

        body.vx += ax * time_scale
        body.vy += ay * time_scale

        body.x += body.vx * time_scale
        body.y += body.vy * time_scale

        if trails:
            body.add_trail()


def black_hole_capture(bodies):
    to_remove = []

    for black_hole in bodies:
        if black_hole.body_type != "black_hole":
            continue

        capture_radius = black_hole.radius + 8

        for other in bodies:
            if other is black_hole:
                continue

            dx = other.x - black_hole.x
            dy = other.y - black_hole.y
            dist = math.sqrt(dx * dx + dy * dy)

            if dist < capture_radius:
                total_mass = black_hole.mass + other.mass

                black_hole.vx = (
                    black_hole.vx * black_hole.mass +
                    other.vx * other.mass
                ) / total_mass

                black_hole.vy = (
                    black_hole.vy * black_hole.mass +
                    other.vy * other.mass
                ) / total_mass

                black_hole.mass = total_mass
                to_remove.append(other)

    for body in to_remove:
        if body in bodies:
            bodies.remove(body)