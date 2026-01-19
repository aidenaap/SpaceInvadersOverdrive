# Space Invaders Overdrive

A classic space invaders game with a twist—collect power-ups to unleash double firepower!

Built to gain familiarity with game development in Python using Pygame.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)

## Controls

| Key | Action |
|-----|--------|
| `W` | Move up |
| `A` | Move left |
| `S` | Move down |
| `D` | Move right |
| `Space` | Shoot |

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Space-Invaders-Overdrive.git
   cd Space-Invaders-Overdrive
   ```

2. Install dependencies:
   ```bash
   pip install pygame numpy
   ```

3. Run the game:
   ```bash
   python SI_OverDrive.py
   ```

## Project Structure

```
Space-Invaders-Overdrive/
├── SI_OverDrive.py
├── README.md
└── Assets/
    ├── spaceship_yellow.png
    ├── spaceship_red.png
    ├── space.png
    └── liquor.png
```

## Gameplay

- Dodge and destroy waves of enemy ships
- Each enemy destroyed awards **10 points**
- You start with **3 lives**
- Enemies spawn in various patterns: left-to-right, right-to-left, converging, and diverging
- Collect the power-up to unlock **dual cannons**

## Technical Overview

### Core Functions

| Function | Description |
|----------|-------------|
| `draw_game_window()` | Renders all game elements to the screen |
| `handle_hero_movement()` | Processes WASD input for player movement |
| `handle_enemy_movement()` | Moves enemies downward and checks for collisions |
| `handle_bullets()` | Updates bullet positions and detects hits |
| `handle_power_movement()` | Moves power-ups down the screen |

### Threaded Functions

The game uses three daemon threads to handle timed spawning independently of the main game loop:

| Thread | Function | Interval |
|--------|----------|----------|
| t1 | `enemy_bullet_spawner()` | Every 1.5 seconds |
| t2 | `ship_spawner()` | Every 7 seconds |
| t3 | `power_up_spawner()` | Every 25-35 seconds (random) |

### Enemy Spawn Patterns

- **acrossleft**: Ships spawn left to right
- **acrossright**: Ships spawn right to left
- **converge**: Ships spawn from edges toward center
- **diverge**: Ships spawn from center toward edges

## Dependencies

- Python 3.8+
- Pygame 2.0+
- NumPy