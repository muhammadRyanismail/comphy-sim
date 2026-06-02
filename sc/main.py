import math
import pygame

from settings import *
from physics import update_nbody, black_hole_capture
from spawner import (
    spawn_black_hole,
    spawn_galactic_core,
    spawn_sun,
    spawn_planet,
    spawn_galaxy,
    create_formation_cloud,
    create_visual_gas_cloud,
    create_visual_spiral,
    create_visual_random_universe,
    create_restricted_merger,
    spawn_rogue_star_cluster,
    spawn_new_starburst,
)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("N-Body Simulation of Galaxy Formation and Evolution")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)
title_font = pygame.font.SysFont("Arial", 40)

bodies = []
particles = []
merger_cores = []

mode = "START"
tool = "GALACTIC CORE"

paused = False
trails = True
gravity_web = False
evolution_start_time = 0
evolution_events_done = set()


def clear_all():
    bodies.clear()
    particles.clear()
    merger_cores.clear()


def set_mode(new_mode):
    global mode, evolution_start_time, evolution_events_done
    mode = new_mode

    if mode == "FORMATION":
        bodies.extend(create_formation_cloud(WIDTH // 2, HEIGHT // 2))

    elif mode == "EVOLUTION":
        bodies.extend(spawn_galaxy(WIDTH // 2, HEIGHT // 2))
        evolution_start_time = pygame.time.get_ticks()
        evolution_events_done = set()

    elif mode == "MERGER":
        cores, stars = create_restricted_merger()
        merger_cores.extend(cores)
        particles.extend(stars)

    elif mode == "GAS CLOUD DEMO":
        particles.extend(create_visual_gas_cloud(WIDTH // 2, HEIGHT // 2))

    elif mode == "SPIRAL DEMO":
        particles.extend(create_visual_spiral(WIDTH // 2, HEIGHT // 2))

    elif mode == "RANDOM DEMO":
        particles.extend(create_visual_random_universe())

def update_merger_cores():
    if len(merger_cores) == 2:
        c1 = merger_cores[0]
        c2 = merger_cores[1]

        dx = c2.x - c1.x
        dy = c2.y - c1.y

        dist_sq = dx * dx + dy * dy + 30000
        dist = math.sqrt(dist_sq)

        a1 = G * c2.mass / dist_sq
        a2 = G * c1.mass / dist_sq

        c1.vx += a1 * dx / dist * TIME_SCALE
        c1.vy += a1 * dy / dist * TIME_SCALE

        c2.vx -= a2 * dx / dist * TIME_SCALE
        c2.vy -= a2 * dy / dist * TIME_SCALE

        # simplified dynamical friction
        c1.vx *= 0.9985
        c1.vy *= 0.9985
        c2.vx *= 0.9985
        c2.vy *= 0.9985

        c1.x += c1.vx * TIME_SCALE
        c1.y += c1.vy * TIME_SCALE

        c2.x += c2.vx * TIME_SCALE
        c2.y += c2.vy * TIME_SCALE

        # when the cores get close enough, merge them into one remnant core
        if dist < 55:
            total_mass = c1.mass + c2.mass

            new_core = spawn_galactic_core(
                (c1.x * c1.mass + c2.x * c2.mass) / total_mass,
                (c1.y * c1.mass + c2.y * c2.mass) / total_mass,
                (c1.vx * c1.mass + c2.vx * c2.mass) / total_mass * 0.4,
                (c1.vy * c1.mass + c2.vy * c2.mass) / total_mass * 0.4,
            )

            new_core.mass = total_mass
            new_core.radius = 8
            new_core.color = (230, 220, 255)

            merger_cores.clear()
            merger_cores.append(new_core)

    elif len(merger_cores) == 1:
        core = merger_cores[0]
        core.x += core.vx * TIME_SCALE
        core.y += core.vy * TIME_SCALE


def update_evolution_events():
    global evolution_events_done

    if mode != "EVOLUTION":
        return

    elapsed = (pygame.time.get_ticks() - evolution_start_time) / 1000

    cx = WIDTH // 2
    cy = HEIGHT // 2

    # Event 1: incoming star cluster
    if elapsed > 8 and "cluster" not in evolution_events_done:
        bodies.extend(
            spawn_rogue_star_cluster(
                WIDTH + 80,
                HEIGHT * 0.35,
                cx,
                cy,
                count=20,
            )
        )
        evolution_events_done.add("cluster")

    # Event 2: new stars appear in the disk
    if elapsed > 18 and "starburst" not in evolution_events_done:
        bodies.extend(
            spawn_new_starburst(
                cx,
                cy,
                count=65,
            )
        )
        evolution_events_done.add("starburst")


def draw_gravity_web():
    draw_list = bodies

    for i in range(0, len(draw_list), 10):
        for j in range(i + 1, min(i + 8, len(draw_list))):
            b1 = draw_list[i]
            b2 = draw_list[j]

            dx = b1.x - b2.x
            dy = b1.y - b2.y

            dist = math.sqrt(dx * dx + dy * dy)

            if dist < 120:
                pygame.draw.line(
                    screen,
                    (70, 50, 130),
                    (b1.x, b1.y),
                    (b2.x, b2.y),
                    1,
                )


def draw_hud():
    hud = [
        f"FPS: {int(clock.get_fps())}",
        f"Mode: {mode}",
        f"Tool: {tool}",
        f"Real N-body bodies: {len(bodies)}",
        f"Visual particles: {len(particles)}",
        "",
        "MAIN MODES",
        "F = Formation",
        "E = Evolution",
        "M = Merger",
        "",
        "VISUAL DEMOS",
        "5 = Gas cloud demo",
        "6 = Spiral demo",
        "7 = Random universe demo",
        "",
        "SANDBOX TOOLS",
        "1 = Galactic core",
        "2 = Black hole",
        "3 = Planet",
        "4 = Sun",
        "Left click = spawn selected tool",
        "",
        "SPACE = Pause",
        "R = Reset",
        "T = Trails",
        "G = Gravity web",
    ]

    y = 10

    for line in hud:
        txt = font.render(line, True, WHITE)
        screen.blit(txt, (10, y))
        y += 22


def draw_start_message():
    if len(bodies) == 0 and len(particles) == 0 and len(merger_cores) == 0:
        txt = title_font.render(
            "N-BODY GALAXY FORMATION AND EVOLUTION",
            True,
            PURPLE,
        )

        screen.blit(
            txt,
            (
                WIDTH // 2 - txt.get_width() // 2,
                HEIGHT // 2 - txt.get_height() // 2 - 30,
            ),
        )

        small = font.render(
            "Press F for Formation, E for Evolution, or M for Merger",
            True,
            WHITE,
        )

        screen.blit(
            small,
            (
                WIDTH // 2 - small.get_width() // 2,
                HEIGHT // 2 + 30,
            ),
        )


running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                set_mode("FORMATION")

            elif event.key == pygame.K_e:
                set_mode("EVOLUTION")

            elif event.key == pygame.K_m:
                set_mode("MERGER")

            elif event.key == pygame.K_5:
                set_mode("GAS CLOUD DEMO")

            elif event.key == pygame.K_6:
                set_mode("SPIRAL DEMO")

            elif event.key == pygame.K_7:
                set_mode("RANDOM DEMO")

            elif event.key == pygame.K_1:
                tool = "GALACTIC CORE"
                mode = "SANDBOX"

            elif event.key == pygame.K_2:
                tool = "BLACK HOLE"
                mode = "SANDBOX"

            elif event.key == pygame.K_3:
                tool = "PLANET"
                mode = "SANDBOX"

            elif event.key == pygame.K_4:
                tool = "SUN"
                mode = "SANDBOX"

            elif event.key == pygame.K_SPACE:
                paused = not paused

            elif event.key == pygame.K_r:
                clear_all()
                mode = "START"

            elif event.key == pygame.K_t:
                trails = not trails

            elif event.key == pygame.K_g:
                gravity_web = not gravity_web

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx, my = pygame.mouse.get_pos()

                # If the user starts clicking, treat it as sandbox mode.
                mode = "SANDBOX"

                if tool == "GALACTIC CORE":
                    bodies.append(spawn_galactic_core(mx, my))

                elif tool == "BLACK HOLE":
                    bodies.append(spawn_black_hole(mx, my))

                elif tool == "PLANET":
                    bodies.append(spawn_planet(mx, my))

                elif tool == "SUN":
                    bodies.append(spawn_sun(mx, my))

    fade = pygame.Surface((WIDTH, HEIGHT))
    fade.set_alpha(32)
    fade.fill(BLACK)
    screen.blit(fade, (0, 0))

    if not paused:
        if mode == "EVOLUTION":
            update_evolution_events()

        if bodies:
            update_nbody(bodies, trails=trails, time_scale=TIME_SCALE)
            black_hole_capture(bodies)

        if mode == "MERGER":
            update_merger_cores()

            for particle in particles:
                particle.update_restricted(
                    merger_cores,
                    g=G,
                    time_scale=TIME_SCALE,
                    damping=0.9997,
                )

        else:
            for particle in particles:
                if mode == "GAS CLOUD DEMO":
                    particle.update_simple()
                elif mode == "SPIRAL DEMO":
                    particle.update_simple()
                elif mode == "RANDOM DEMO":
                    particle.update_simple()
                else:
                    particle.update_simple()

    if gravity_web:
        draw_gravity_web()

    for body in bodies:
        body.draw(screen, trails=trails)

    for core in merger_cores:
        core.draw(screen, trails=False)

    for particle in particles:
        particle.draw(screen, trails=(mode == "MERGER" and trails))

    draw_hud()
    draw_start_message()

    pygame.display.flip()

pygame.quit()