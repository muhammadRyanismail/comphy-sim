import pygame

from settings import *
from physics import update_body

from spawner import (
    spawn_galaxy,
    spawn_blackhole,
    spawn_planet,
    spawn_sun
)

pygame.init()

screen = pygame.display.set_mode(
    (WIDTH,HEIGHT)
)

pygame.display.set_caption(
    "Cosmic Sandbox"
)

clock = pygame.time.Clock()

font = pygame.font.SysFont(
    "Arial",
    20
)

MODE = "GALAXY"

TRAILS = True

paused = False

bodies = []

running = True

while running:

    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_1:
                MODE = "GALAXY"

            elif event.key == pygame.K_2:
                MODE = "BLACKHOLE"

            elif event.key == pygame.K_3:
                MODE = "PLANET"

            elif event.key == pygame.K_4:
                MODE = "SUN"

            elif event.key == pygame.K_SPACE:
                paused = not paused

            elif event.key == pygame.K_r:
                bodies.clear()

            elif event.key == pygame.K_t:
                TRAILS = not TRAILS

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                x,y = pygame.mouse.get_pos()

                if MODE == "GALAXY":
                    bodies.extend(
                        spawn_galaxy(x,y)
                    )

                elif MODE == "BLACKHOLE":
                    bodies.append(
                        spawn_blackhole(x,y)
                    )

                elif MODE == "PLANET":
                    bodies.append(
                        spawn_planet(x,y)
                    )

                elif MODE == "SUN":
                    bodies.append(
                        spawn_sun(x,y)
                    )

    screen.fill(BLACK)

    if not paused:

        for body in bodies:

            update_body(
                body,
                bodies,
                TRAILS,
                TIME_SCALE
            )

    for body in bodies:
        body.draw(
            screen,
            TRAILS
        )

    hud = [

        f"FPS: {int(clock.get_fps())}",
        f"Objects: {len(bodies)}",
        f"Mode: {MODE}",
        "",
        "1 = Galaxy",
        "2 = Black Hole",
        "3 = Planet",
        "4 = Sun",
        "",
        "Click = Spawn",
        "SPACE = Pause",
        "R = Reset",
        "T = Trails"
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

    pygame.display.flip()

pygame.quit()