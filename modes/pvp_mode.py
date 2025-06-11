import pygame
import os
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, MAX_HEALTH, MAX_ENERGY
from hud.health_bar import draw_health_bar
from hud.energy_bar import draw_energy_bar
from controls import PLAYER1_CONTROLS, PLAYER2_CONTROLS
from scenes.battle_scene import (
    load_tile_frames, get_character_positions, new_player,
    get_default_damage, draw_timer, show_KO,
    handle_round_winner, reset_round, draw_round_label, draw_round_wins,
    draw_debug_hitboxes
)
from scenes.result_screen import show_win_screen
from stage.stage import Stage

# === Constants ===
LEFT_BOUND = 20
RIGHT_BOUND = SCREEN_WIDTH - 200

pygame.mixer.init()
pygame.init()
# === Sound Effects ===
SFX = {
    "punch": pygame.mixer.Sound("D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/sfx/punch.wav"),
    "punch_block": pygame.mixer.Sound("D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/sfx/punch_block.wav"),
    "punch_no_hit": pygame.mixer.Sound("D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/sfx/punch_no_hit.wav"),
    "kick": pygame.mixer.Sound("D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/sfx/kick.wav"),
    "kick_block": pygame.mixer.Sound("D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/sfx/kick_block.wav"),
    "kick_no_hit": pygame.mixer.Sound("D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/sfx/kick_no_hit.wav"),
    "special": pygame.mixer.Sound("D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/sfx/special.wav"),
}

def get_body_hitbox(player):
    name = player["name"]
    x, y = player["x"], player["y"]
    if name in ["Junli", "Cammy"]:
        return pygame.Rect(x + 35, y + 20, 90, 240)
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

def load_animations(character_folder):
    animations = {}
    for move in ["Idle", "Walk", "Jab", "Kick", "Block", "Crouch", "Jump", "Jump Forward", "Special"]:
        move_folder = os.path.join(character_folder, move)
        if os.path.exists(move_folder):
            frames = [f for f in os.listdir(move_folder) if f.endswith('.png')]
            if frames:
                animations[move] = load_tile_frames(move_folder, len(frames), scale=2.5)
    return animations

def run_pvp_battle(p1_name, p2_name, stage_name):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 32)

    stage = Stage(stage_name)

    character_folders = {
        "Junli": "Character 1", "Kay": "Character 2",
        "Cammy": "Character 3", "Guile": "Character 4"
    }

    p1_anims = load_animations(f"D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/characters/{character_folders[p1_name]}")
    p2_anims = load_animations(f"D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/characters/{character_folders[p2_name]}")
    positions = get_character_positions()
    _, p1_y = positions[p1_name]
    _, p2_y = positions[p2_name]
    p1 = new_player(p1_name, p1_anims, 150, p1_y)
    p2 = new_player(p2_name, p2_anims, 900, p2_y)

    damage_values = get_default_damage()
    gravity, jump_power = 1.2, -18
    frame_delay = 100
    last_update = pygame.time.get_ticks()
    attack_cooldown = 500
    round_start = pygame.time.get_ticks()
    round_time_limit = 120
    scores = {"p1": 0, "p2": 0}

    running = True
    while running:
        screen.fill((0, 0, 0))
        now = pygame.time.get_ticks()

        stage.update()
        stage.draw(screen, opacity=255)

        if draw_timer(screen, font, round_start, round_time_limit) == 0 or p1["health"] <= 0 or p2["health"] <= 0:
            winner = handle_round_winner(p1, p2, scores)
            show_KO(screen)
            if scores["p1"] == 2 or scores["p2"] == 2:
                show_win_screen(screen, p1_name if scores["p1"] == 2 else p2_name)
                return
            round_start = reset_round(p1, p2)

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                for p, controls in [(p1, PLAYER1_CONTROLS), (p2, PLAYER2_CONTROLS)]:
                    if now - p["last_attack"] >= attack_cooldown:
                        if event.key == controls["punch"]:
                            p["state"], p["frames"], p["frame"] = "Jab", p["anims"]["Jab"], 0
                            p["last_attack"] = now
                        elif event.key == controls["kick"]:
                            p["state"], p["frames"], p["frame"] = "Kick", p["anims"]["Kick"], 0
                            p["last_attack"] = now
                        elif event.key == controls["special"] and p["energy"] == MAX_ENERGY:
                            p["state"], p["frames"], p["frame"], p["energy"] = "Special", p["anims"]["Special"], 0, 0
                            SFX["special"].play()

        for p, controls in [(p1, PLAYER1_CONTROLS), (p2, PLAYER2_CONTROLS)]:
            if p["on_ground"]:
                if keys[controls["crouch"]]:
                    if p["state"] != "Crouch":
                        p["state"], p["frames"], p["frame"] = "Crouch", p["anims"]["Crouch"], 0
                elif keys[controls["block"]]:
                    if p["state"] != "Block":
                        p["state"], p["frames"], p["frame"] = "Block", p["anims"]["Block"], 0
                elif keys[controls["left"]]:
                    p["x"] -= 5
                    p["state"], p["frames"] = "Walk", p["anims"]["Walk"]
                elif keys[controls["right"]]:
                    p["x"] += 5
                    p["state"], p["frames"] = "Walk", p["anims"]["Walk"]
                else:
                    if p["state"] in ["Walk", "Crouch", "Block"]:
                        p["state"], p["frames"], p["frame"] = "Idle", p["anims"]["Idle"], 0

            if keys[controls["up"]] and p["on_ground"]:
                p["state"] = "Jump Forward" if keys[controls["left"]] or keys[controls["right"]] else "Jump"
                p["frames"] = p["anims"][p["state"]]
                p["vx"] = -5 if keys[controls["left"]] else 5 if keys[controls["right"]] else 0
                p["vy"] = jump_power
                p["on_ground"], p["frame"] = False, 0

            if not p["on_ground"]:
                fall_speed = gravity * (0.6 if p["state"] == "Jump Forward" else 1)
                p["vy"] += fall_speed
                p["y"] += p["vy"]
                p["x"] += p["vx"]
                if p["y"] >= p["base_y"]:
                    p["y"], p["vy"], p["vx"] = p["base_y"], 0, 0
                    p["on_ground"], p["state"], p["frames"], p["frame"] = True, "Idle", p["anims"]["Idle"], 0

            p["x"] = max(LEFT_BOUND, min(p["x"], RIGHT_BOUND))

        if now - last_update > frame_delay:
            for attacker, target in [(p1, p2), (p2, p1)]:
                if attacker["state"] in ["Jab", "Kick", "Special"]:
                    if attacker["frame"] < len(attacker["frames"]) - 1:
                        attacker["frame"] += 1
                    else:
                        atk_type = attacker["state"]
                        atk_rect = get_attack_hitbox(attacker, target)
                        body_rect = get_body_hitbox(target)
                        hit = atk_rect.colliderect(body_rect)

                        if atk_type == "Jab":
                            if hit:
                                if target["state"] == "Block":
                                    SFX["punch_block"].play()
                                else:
                                    SFX["punch"].play()
                            else:
                                SFX["punch_no_hit"].play()
                        elif atk_type == "Kick":
                            if hit:
                                if target["state"] == "Block":
                                    SFX["kick_block"].play()
                                else:
                                    SFX["kick"].play()
                            else:
                                SFX["kick_no_hit"].play()

                        if hit:
                            dmg = damage_values[atk_type]
                            if target["state"] == "Block":
                                dmg = max(0, dmg - damage_values["Block_Reduction"])
                            target["health"] = max(0, target["health"] - dmg)
                            if atk_type in ["Jab", "Kick"]:
                                attacker["energy"] = min(MAX_ENERGY, attacker["energy"] + damage_values["Energy_Gain"])

                        attacker["state"], attacker["frames"], attacker["frame"] = "Idle", attacker["anims"]["Idle"], 0
                elif attacker["state"] in ["Crouch", "Block"]:
                    attacker["frame"] = min(attacker["frame"], len(attacker["frames"]) - 1)
                else:
                    attacker["frame"] = (attacker["frame"] + 1) % len(attacker["frames"])
            last_update = now

        p1_flipped = p1["x"] > p2["x"]
        p2_flipped = not p1_flipped
        screen.blit(pygame.transform.flip(p1["frames"][p1["frame"]], p1_flipped, False), (p1["x"], p1["y"]))
        screen.blit(pygame.transform.flip(p2["frames"][p2["frame"]], p2_flipped, False), (p2["x"], p2["y"]))
        draw_health_bar(screen, p1["health"], (50, 65))
        draw_energy_bar(screen, p1["energy"], (50, 95))
        draw_health_bar(screen, p2["health"], (SCREEN_WIDTH - 350, 65))
        draw_energy_bar(screen, p2["energy"], (SCREEN_WIDTH - 350, 95))
        screen.blit(font.render(p1_name, True, (255, 255, 255)), (50, 20))
        screen.blit(font.render(p2_name, True, (255, 255, 255)), (SCREEN_WIDTH - 105, 20))
        draw_round_label(screen, font, scores["p1"], scores["p2"])
        draw_round_wins(screen, font, scores["p1"], scores["p2"])

        pygame.display.flip()
        clock.tick(FPS)

    return
