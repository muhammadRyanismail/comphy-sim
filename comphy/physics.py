import math
from settings import G

def update_body(body,bodies,trails,time_scale):

    if body.fixed:
        return

    ax = 0
    ay = 0

    for other in bodies:

        if other == body:
            continue

        dx = other.x - body.x
        dy = other.y - body.y

        dist_sq = dx*dx + dy*dy + 25

        dist = math.sqrt(dist_sq)

        force = (
            G *
            body.mass *
            other.mass /
            dist_sq
        )

        ax += force * dx / dist / body.mass
        ay += force * dy / dist / body.mass

    body.vx += ax * time_scale
    body.vy += ay * time_scale

    body.x += body.vx * time_scale
    body.y += body.vy * time_scale

    if trails:

        body.trail.append(
            (body.x,body.y)
        )

        if len(body.trail) > 30:
            body.trail.pop(0)