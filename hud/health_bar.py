# hud/health_bar.py
# Draws the health bar UI for a fighter based on their current HP.

import pygame
from config import MAX_HEALTH, RED, GREEN, WHITE

def draw_health_bar(screen, current_hp, position):
    bar_width = 300
    bar_height = 25
    x, y = position

    # Background border
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, bar_width + 4, bar_height + 4))

    # Background (empty bar)
    pygame.draw.rect(screen, RED, (x, y, bar_width, bar_height))

    # Filled health (green)
    health_ratio = max(0, current_hp / MAX_HEALTH)
    filled_width = int(bar_width * health_ratio)
    pygame.draw.rect(screen, GREEN, (x, y, filled_width, bar_height))
