# N-Body Simulation of Galaxy Formation and Evolution

## Project Overview

This project implements a 2D N-body simulation of galaxy formation, evolution, and galaxy mergers using Newtonian gravity. The simulation was developed in Python using Pygame and demonstrates how gravitational interactions can produce large-scale galactic structures.

The project was created as part of a Computational Physics course and includes multiple simulation modes that visualize different astrophysical processes.

---

## Requirements

* Python 3.x
* Pygame

Install Pygame:

```bash
pip install pygame
```

---

## Run

```bash
python main.py
```

---

## Simulation Modes

### F = Formation Mode

Real direct N-body simulation.

* Starts with a rotating cloud of particles.
* Gravity causes particles to collapse toward dense regions.
* Galaxy-like structures emerge naturally through gravitational interactions.
* Demonstrates simplified galaxy formation.

### E = Evolution Mode

Real direct N-body simulation.

* Starts with an already formed galaxy.
* Demonstrates long-term galactic evolution.
* A rogue star cluster enters the system and perturbs stellar orbits.
* A simplified starburst event generates new stars near the galactic center.
* Shows how internal and external influences can alter galactic structure over time.

### M = Merger Mode

Restricted N-body approximation.

* Two galaxies are initialized separately.
* Massive galactic cores interact gravitationally.
* Stars are represented as visual test particles affected by the galaxy cores.
* Produces tidal distortions and eventual galaxy merger.
* More efficient than a full O(N²) merger simulation.

---

## Visual Demo Modes

### 5 = Gas Cloud Demo

Original visual demonstration.

* Particles drift inward using preset velocities.
* Not a true N-body galaxy formation simulation.

### 6 = Spiral Demo

Original visual demonstration.

* Spiral structure is generated mathematically.
* Not a true galaxy formation simulation.

### 8 = Random Universe Demo

Original visual demonstration.

* Random particles move with randomized motion.
* Not a true N-body simulation.

---

## Sandbox Tools

### Object Selection

* 1 = Galactic Core
* 2 = Black Hole
* 3 = Planet
* 4 = Sun

### Placement

* Left Click = Spawn selected object

Sandbox mode allows users to create and interact with custom gravitational systems.

---

## Controls

| Key   | Function             |
| ----- | -------------------- |
| F     | Formation Mode       |
| E     | Evolution Mode       |
| M     | Merger Mode          |
| 5     | Gas Cloud Demo       |
| 6     | Spiral Demo          |
| 8     | Random Universe Demo |
| 1     | Select Galactic Core |
| 2     | Select Black Hole    |
| 3     | Select Planet        |
| 4     | Select Sun           |
| SPACE | Pause / Resume       |
| R     | Reset Current Mode   |
| T     | Toggle Trails        |
| G     | Toggle Gravity Web   |

---

## Physics Model

The simulation is based on Newton's Law of Universal Gravitation:

F = G(m₁m₂/r²)

Each body exerts a gravitational force on every other body in the system.

The simulation updates particle motion using Euler Integration:

v(t+Δt) = v(t) + aΔt

x(t+Δt) = x(t) + vΔt

---

## Numerical Method

The simulation uses:

* Newtonian gravity
* Direct O(N²) force calculations
* Euler Integration
* Gravitational softening for stability

The merger mode uses a restricted N-body approximation to improve performance.

---

## Computational Complexity

For direct N-body simulation:

O(N²)

Every particle interacts with every other particle, causing the number of force calculations to increase rapidly as the particle count grows.

---

## Limitations

This simulation is intended for educational visualization purposes and includes several simplifications:

* Two-dimensional simulation
* Newtonian gravity only
* Euler Integration introduces numerical error over time
* No dark matter modeling
* No gas dynamics
* No relativistic effects
* No realistic stellar evolution
* No realistic star formation physics
* Uses normalized simulation units rather than real astronomical units

The starburst event is represented by generating new particles and does not model actual astrophysical star formation processes.

---

## Authors

### Irene Angelina (2802501060)

* Research and literature review
* Report writing
* Presentation preparation
* Testing and validation
* Simulation enhancements and feature improvements

### Muhammad Ryan Ismail Putra (2802522733)

* Initial simulation implementation
* Base N-body system development
* Pygame framework setup
* Presentation template design
* Research

---

## Course Information

Computational Physics (SCIE6063001)

Final Project

N-Body Simulation of Galaxy Formation and Evolution