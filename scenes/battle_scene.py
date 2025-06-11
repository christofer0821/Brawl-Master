import pygame
import os
from config import SCREEN_WIDTH, SCREEN_HEIGHT, MAX_HEALTH, MAX_ENERGY

def create_hitbox(x, y, w, h):
    return pygame.Rect(x, y, w, h)

def load_tile_frames(folder, count, scale=None, flip=False):
    frames = []
    for i in range(count):
        path = os.path.join(folder, f"tile00{i}.png")
        img = pygame.image.load(path).convert_alpha()
        if scale:
            scaled = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        else:
            base_height = 180
            scale_factor = base_height / img.get_height()
            scaled = pygame.transform.scale(img, (int(img.get_width() * scale_factor), int(img.get_height() * scale_factor)))
        if flip:
            scaled = pygame.transform.flip(scaled, True, False)
        frames.append(scaled)
    return frames

def get_character_positions():
    return {
        "Kay": (150, 400),
        "Junli": (150, 450),
        "Cammy": (150, 450),
        "Guile": (150, 400)
    }

def new_player(name, anims, x, y, max_health=MAX_HEALTH, max_energy=MAX_ENERGY):
    return {
        "name": name,
        "x": x, "y": y, "vx": 0, "vy": 0, "on_ground": True,
        "state": "Idle", "frame": 0, "health": max_health, "energy": 0,
        "anims": anims, "frames": anims["Idle"], "last_attack": 0,
        "base_y": y
    }

def get_default_damage():
    return {
        "Jab": 10,
        "Kick": 10,
        "Special": 20,
        "Block_Reduction": 5,
        "Energy_Gain": 20
    }

def draw_timer(screen, font, start_ticks, total_seconds):
    remaining = max(0, total_seconds - (pygame.time.get_ticks() - start_ticks) // 1000)
    timer = font.render(str(remaining), True, (255, 255, 0))
    screen.blit(timer, (SCREEN_WIDTH // 2 - timer.get_width() // 2, 20))
    return remaining

def show_KO(screen):
    ko_img = pygame.image.load("D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/stages/KO.png").convert_alpha()
    ko_sound_path = "D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/music/ko_sound.wav"
    pygame.mixer.init()
    pygame.mixer.music.load(ko_sound_path)
    pygame.mixer.music.play()
    clock = pygame.time.Clock()
    for scale in range(10, 101, 5):
        scaled = pygame.transform.scale(ko_img, (scale * 6, scale * 3))
        screen.blit(scaled, (
            SCREEN_WIDTH // 2 - scaled.get_width() // 2,
            SCREEN_HEIGHT // 2 - scaled.get_height() // 2
        ))
        pygame.display.flip()
        clock.tick(30)
    pygame.time.delay(1200)
    for alpha in range(255, 0, -12):
        faded = ko_img.copy()
        faded.set_alpha(alpha)
        scaled = pygame.transform.scale(faded, (600, 300))
        screen.blit(scaled, (
            SCREEN_WIDTH // 2 - scaled.get_width() // 2,
            SCREEN_HEIGHT // 2 - scaled.get_height() // 2
        ))
        pygame.display.flip()
        clock.tick(30)
    pygame.mixer.music.stop()

def handle_round_winner(p1, p2, scores):
    if p1["health"] <= 0:
        scores["p2"] += 1
        return "p2"
    elif p2["health"] <= 0:
        scores["p1"] += 1
        return "p1"
    return None

def reset_round(p1, p2):
    p1.update({"health": MAX_HEALTH, "energy": 0, "x": 150, "y": p1["base_y"], "frame": 0, "state": "Idle", "frames": p1["anims"]["Idle"]})
    p2.update({"health": MAX_HEALTH, "energy": 0, "x": 900, "y": p2["base_y"], "frame": 0, "state": "Idle", "frames": p2["anims"]["Idle"]})
    return pygame.time.get_ticks()

def draw_round_label(screen, font, p1_score, p2_score):
    if p1_score == 1 and p2_score == 1:
        label = "Final Round"
    elif p1_score + p2_score == 0:
        label = "Round 1"
    elif p1_score + p2_score == 1:
        label = "Round 2"
    else:
        return
    text = font.render(label, True, (255, 0, 0))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 70))

def draw_round_wins(screen, font, p1_score, p2_score):
    red = "🔴" * p1_score
    green = "🟢" * p2_score
    text = font.render(f"{red}   {green}", True, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 95))

def draw_debug_hitboxes(screen, p1, p2):
    def get_body_hitbox(player):
        name = player["name"]
        x, y = player["x"], player["y"]
        if name in ["Junli", "Cammy"]:
            return pygame.Rect(x + 35, y + 20, 100, 240)
        else:
            return pygame.Rect(x + 30, y, 110, 280)

    def get_attack_hitbox(player, opponent):
        name = player["name"]
        x, y = player["x"], player["y"]
        facing_left = x > opponent["x"]
        if name in ["Junli", "Cammy"]:
            return pygame.Rect(x - 70 if facing_left else x + 110, y + 40, 50, 30)
        else:
            return pygame.Rect(x - 30 if facing_left else x + 120, y + 100, 60, 30)

    # Draw body hitboxes
    p1_body = get_body_hitbox(p1)
    p2_body = get_body_hitbox(p2)
    pygame.draw.rect(screen, (0, 0, 255), p1_body, 2)
    pygame.draw.rect(screen, (0, 0, 255), p2_body, 2)

    # Draw attack hitboxes
    if p1["state"] in ["Jab", "Kick", "Special"]:
        atk_range = get_attack_hitbox(p1, p2)
        pygame.draw.rect(screen, (255, 0, 0), atk_range, 2)
    if p2["state"] in ["Jab", "Kick", "Special"]:
        atk_range = get_attack_hitbox(p2, p1)
        pygame.draw.rect(screen, (255, 0, 0), atk_range, 2)
