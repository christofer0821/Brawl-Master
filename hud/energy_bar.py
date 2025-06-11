# hud/energy_bar.py
# Draws the energy meter and cooldown indicator.

import pygame
from config import MAX_ENERGY, BLUE, WHITE

def draw_energy_bar(screen, current_energy, position):
    bar_width = 300
    bar_height = 20
    x, y = position

    # Border
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, bar_width + 4, bar_height + 4))

    # Fill
    energy_ratio = max(0, current_energy / MAX_ENERGY)
    filled_width = int(bar_width * energy_ratio)
    pygame.draw.rect(screen, BLUE, (x, y, filled_width, bar_height))