import pygame
import sys
import os
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, MAX_ENERGY
from controls import PLAYER1_CONTROLS
from scenes.character_select import character_select
from scenes.battle_scene import (
    load_tile_frames, get_character_positions, new_player,
    draw_timer, show_KO, draw_round_label, draw_round_wins
)
from scenes.result_screen import show_win_screen, show_lose_screen, set_return_callback
from hud.health_bar import draw_health_bar
from hud.energy_bar import draw_energy_bar
from stage.stage import Stage
from character.bot import update_bot
from moviepy import VideoFileClip

LEFT_BOUND = 20
RIGHT_BOUND = SCREEN_WIDTH - 200

def play_cutscene(path):
    clip = VideoFileClip(path)
    clip.preview()
    clip.close()

    pygame.display.quit()
    pygame.display.init()
    return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # re-init display

def get_body_hitbox(player):
    x, y = player["x"], player["y"]
    return pygame.Rect(x + 35, y + 20, 100, 240) if player["name"] in ["Junli", "Cammy"] else pygame.Rect(x + 30, y, 110, 280)

def get_attack_hitbox(player, opponent):
    x, y = player["x"], player["y"]
    facing_left = x > opponent["x"]
    if player["name"] in ["Junli", "Cammy"]:
        return pygame.Rect(x - 70 if facing_left else x + 110, y + 40, 50, 30)
    else:
        return pygame.Rect(x - 30 if facing_left else x + 120, y + 100, 60, 30)

def load_animations(folder):
    animations = {}
    for move in ["Idle", "Walk", "Jab", "Kick", "Block", "Crouch", "Jump", "Jump Forward", "Special"]:
        move_path = os.path.join(folder, move)
        if os.path.exists(move_path):
            frames = [f for f in os.listdir(move_path) if f.endswith('.png')]
            if frames:
                animations[move] = load_tile_frames(move_path, len(frames), scale=2.5)
    return animations

def extract_y(pos, default_y=450):
    return pos[1] if isinstance(pos, (list, tuple)) and len(pos) >= 2 else default_y

def load_sounds():
    return {
        "special": pygame.mixer.Sound("assets/sfx/special.wav"),
        "kick": pygame.mixer.Sound("assets/sfx/kick.wav"),
        "kick_block": pygame.mixer.Sound("assets/sfx/kick_block.wav"),
        "kick_no_hit": pygame.mixer.Sound("assets/sfx/kick_no_hit.wav"),
        "punch": pygame.mixer.Sound("assets/sfx/punch.wav"),
        "punch_block": pygame.mixer.Sound("assets/sfx/punch_block.wav"),
        "punch_no_hit": pygame.mixer.Sound("assets/sfx/punch_no_hit.wav"),
        "countdown": pygame.mixer.Sound("assets/music/3 2 1 fight Sound effect.wav")
    }

def animated_countdown(screen, font, sound):
    text_sequence = ["3", "2", "1", "FIGHT!"]
    sound.play()
    for text in text_sequence:
        for size in range(30, 120, 5):
            screen.fill((0, 0, 0))
            rendered = font.render(text, True, (255, 255, 255))
            rect = rendered.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(rendered, rect)
            pygame.display.flip()
            pygame.time.delay(30)
        pygame.time.delay(400)

def run_story_mode():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.SysFont("Arial", 36)
    sounds = load_sounds()

    pygame.mixer.music.load("assets/music/Character_Select_Theme.wav")
    pygame.mixer.music.play(-1)
    player_character = character_select(screen, font)
    pygame.mixer.music.stop()

    screen = play_cutscene("assets/Cut scene/opening_scene.mp4")

    folders = {
        "Junli": "Character 1", "Kay": "Character 2",
        "Cammy": "Character 3", "Guile": "Character 4"
    }

    levels = [
        {"stage": "Champion Ring", "bot": "Cammy", "level": 1},
        {"stage": "Street of Art", "bot": "Guile", "level": 2},
        {"stage": "Dragon Temple", "bot": "Junli", "level": 3},
    ]

    current_level = 0

    def run_level():
        nonlocal current_level
        clock = pygame.time.Clock()
        level_data = levels[current_level]
        cooldown = {1: 900, 2: 1200, 3: 1500}[level_data["level"]]

        stage = Stage(level_data["stage"])
        p1_anims = load_animations(f"assets/characters/{folders[player_character]}")
        bot_anims = load_animations(f"assets/characters/{folders[level_data['bot']]}")

        y_pos = get_character_positions()
        p1_y = extract_y(y_pos.get(player_character))
        bot_y = extract_y(y_pos.get(level_data["bot"]))

        p1 = new_player(player_character, p1_anims, 150, p1_y)
        bot = new_player(level_data["bot"], bot_anims, 900, bot_y)

        gravity, jump_power, frame_delay = 1.2, -18, 100
        last_update = pygame.time.get_ticks()
        round_start = pygame.time.get_ticks()
        round_time_limit = 120

        def go_to_next_level():
            nonlocal current_level
            current_level += 1
            if current_level < len(levels):
                run_level()
            else:
                # Return to mode menu after story ends
                from main import slide_left_transition, mode_menu
                slide_left_transition(mode_menu)

        def retry_this_level():
            run_level()

        screen.fill((0, 0, 0))
        pygame.display.flip()
        animated_countdown(screen, font, sounds["countdown"])

        running = True
        while running:
            screen.fill((0, 0, 0))
            now = pygame.time.get_ticks()
            stage.update()
            stage.draw(screen)

            seconds_left = draw_timer(screen, font, round_start, round_time_limit)
            if seconds_left == 0 or p1["health"] <= 0 or bot["health"] <= 0:
                show_KO(screen)
                pygame.time.delay(1000)
                pygame.event.clear()
                if bot["health"] <= 0:
                    set_return_callback(go_to_next_level)
                    show_win_screen(screen, p1["name"])
                else:
                    set_return_callback(retry_this_level)
                    show_lose_screen(screen, p1["name"])
                return

            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                elif event.type == pygame.KEYDOWN and now - p1["last_attack"] >= 500:
                    if event.key == PLAYER1_CONTROLS["punch"]:
                        p1["state"], p1["frames"], p1["frame"] = "Jab", p1["anims"]["Jab"], 0
                        p1["last_attack"] = now
                    elif event.key == PLAYER1_CONTROLS["kick"]:
                        p1["state"], p1["frames"], p1["frame"] = "Kick", p1["anims"]["Kick"], 0
                        p1["last_attack"] = now
                    elif event.key == PLAYER1_CONTROLS["special"] and p1["energy"] == MAX_ENERGY:
                        p1["state"], p1["frames"], p1["frame"], p1["energy"] = "Special", p1["anims"]["Special"], 0, 0
                        sounds["special"].play()

            if p1["on_ground"]:
                if keys[PLAYER1_CONTROLS["crouch"]]:
                    p1["state"], p1["frames"], p1["frame"] = "Crouch", p1["anims"]["Crouch"], 0
                elif keys[PLAYER1_CONTROLS["block"]]:
                    p1["state"], p1["frames"], p1["frame"] = "Block", p1["anims"]["Block"], 0
                elif keys[PLAYER1_CONTROLS["left"]]:
                    p1["x"] -= 5
                    p1["state"], p1["frames"] = "Walk", p1["anims"]["Walk"]
                elif keys[PLAYER1_CONTROLS["right"]]:
                    p1["x"] += 5
                    p1["state"], p1["frames"] = "Walk", p1["anims"]["Walk"]
                else:
                    if p1["state"] in ["Crouch", "Block", "Walk"]:
                        p1["state"], p1["frames"], p1["frame"] = "Idle", p1["anims"]["Idle"], 0

            if keys[PLAYER1_CONTROLS["up"]] and p1["on_ground"]:
                p1["state"] = "Jump Forward" if keys[PLAYER1_CONTROLS["left"]] or keys[PLAYER1_CONTROLS["right"]] else "Jump"
                p1["frames"] = p1["anims"][p1["state"]]
                p1["vx"] = -5 if keys[PLAYER1_CONTROLS["left"]] else 5 if keys[PLAYER1_CONTROLS["right"]] else 0
                p1["vy"] = jump_power
                p1["on_ground"], p1["frame"] = False, 0

            if not p1["on_ground"]:
                p1["vy"] += gravity
                p1["y"] += p1["vy"]
                p1["x"] += p1["vx"]
                if p1["y"] >= p1["base_y"]:
                    p1["y"], p1["vy"], p1["vx"] = p1["base_y"], 0, 0
                    p1["on_ground"], p1["state"], p1["frames"], p1["frame"] = True, "Idle", p1["anims"]["Idle"], 0

            p1["x"] = max(LEFT_BOUND, min(p1["x"], RIGHT_BOUND))
            bot["x"] = max(LEFT_BOUND, min(bot["x"], RIGHT_BOUND))

            bot, bot_damage = update_bot(bot, p1, now, cooldown, level_data["level"])

            if now - last_update > frame_delay:
                for attacker, target, dmg_source in [(p1, bot, {
                    "Jab": 10, "Kick": 10, "Special": 20, "Block_Reduction": 5, "Energy_Gain": 20
                }), (bot, p1, bot_damage)]:
                    if attacker["state"] in ["Jab", "Kick", "Special"]:
                        if attacker["frame"] < len(attacker["frames"]) - 1:
                            attacker["frame"] += 1
                        else:
                            hit = get_attack_hitbox(attacker, target).colliderect(get_body_hitbox(target))
                            if hit:
                                dmg = dmg_source[attacker["state"]]
                                if target["state"] == "Block":
                                    dmg = max(0, dmg - dmg_source["Block_Reduction"])
                                target["health"] = max(0, target["health"] - dmg)
                                if attacker["state"] in ["Jab", "Kick"]:
                                    attacker["energy"] = min(MAX_ENERGY, attacker["energy"] + dmg_source["Energy_Gain"])
                            attacker["state"], attacker["frames"], attacker["frame"] = "Idle", attacker["anims"]["Idle"], 0
                    else:
                        attacker["frame"] = (attacker["frame"] + 1) % len(attacker["frames"])
                last_update = now

            p1_flipped = p1["x"] > bot["x"]
            bot_flipped = not p1_flipped
            screen.blit(pygame.transform.flip(p1["frames"][p1["frame"]], p1_flipped, False), (p1["x"], p1["y"]))
            screen.blit(pygame.transform.flip(bot["frames"][bot["frame"]], bot_flipped, False), (bot["x"], bot["y"]))

            draw_health_bar(screen, p1["health"], (50, 65))
            draw_energy_bar(screen, p1["energy"], (50, 95))
            draw_health_bar(screen, bot["health"], (SCREEN_WIDTH - 350, 65))
            draw_energy_bar(screen, bot["energy"], (SCREEN_WIDTH - 350, 95))
            screen.blit(font.render(p1["name"], True, (255, 255, 255)), (50, 20))
            screen.blit(font.render(bot["name"], True, (255, 255, 255)), (SCREEN_WIDTH - 105, 20))
            draw_round_label(screen, font, 0, 0)
            draw_round_wins(screen, font, 0, 0)

            pygame.display.flip()
            clock.tick(FPS)

    run_level()
