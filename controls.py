# controls.py
import pygame

PLAYER1_CONTROLS = {
    "punch": pygame.K_h,
    "kick": pygame.K_j,
    "special": pygame.K_k,
    "block": pygame.K_l,
    "crouch": pygame.K_s,
    "up": pygame.K_w,
    "left": pygame.K_a,
    "right": pygame.K_d,
}

PLAYER2_CONTROLS = {
    "punch": pygame.K_KP1,
    "kick": pygame.K_KP2,
    "special": pygame.K_KP3,
    "block": pygame.K_KP4,
    "crouch": pygame.K_DOWN,
    "up": pygame.K_UP,
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
}
