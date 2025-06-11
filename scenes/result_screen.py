import pygame
import os
from config import SCREEN_WIDTH, SCREEN_HEIGHT

# Internal global to store the actual callback function
__return_callback_func = None


def set_return_callback(callback_func):
    global __return_callback_func
    __return_callback_func = callback_func


def call_return_callback():
    if __return_callback_func:
        __return_callback_func()


def load_win_animation(folder, scale=2.5):
    frames = []
    for file in sorted(os.listdir(folder)):
        if file.endswith(".png"):
            img = pygame.image.load(os.path.join(folder, file)).convert_alpha()
            scaled = pygame.transform.scale(img, (
                int(img.get_width() * scale),
                int(img.get_height() * scale)
            ))
            frames.append(scaled)
    return frames


def load_you_win_frames():
    folder = "D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/Logo 3"
    return [
        pygame.transform.scale(
            pygame.image.load(os.path.join(folder, file)).convert_alpha(),
            (700, 180)
        )
        for file in sorted(os.listdir(folder)) if file.endswith(".png")
    ]


def load_you_lose_frames():
    folder = "D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/Logo 4"
    return [
        pygame.transform.scale(
            pygame.image.load(os.path.join(folder, file)).convert_alpha(),
            (700, 180)
        )
        for file in sorted(os.listdir(folder)) if file.endswith(".png")
    ]


def play_victory_music(path):
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(-1)


def show_win_screen(screen, winner_name):
    pygame.init()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 36)

    win_folders = {
        "Cammy": "Character 3",
        "Junli": "Character 1",
        "Kay": "Character 2",
        "Guile": "Character 4"
    }
    win_folder = f"D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/characters/{win_folders[winner_name]}/win"
    win_frames = load_win_animation(win_folder)
    you_win_frames = load_you_win_frames()

    frame_index = 0
    win_text_index = 0

    play_victory_music("D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/music/Victory_Theme.wav")

    prompt_text = font.render("Press any key to next level", True, (255, 255, 255))
    prompt_pos = (
        SCREEN_WIDTH // 2 - prompt_text.get_width() // 2,
        SCREEN_HEIGHT - 100
    )

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(you_win_frames[win_text_index], (SCREEN_WIDTH // 2 - 350, 40))
        screen.blit(win_frames[frame_index], (
            SCREEN_WIDTH // 2 - win_frames[frame_index].get_width() // 2,
            SCREEN_HEIGHT // 2 - win_frames[frame_index].get_height() // 2 + 40
        ))
        screen.blit(prompt_text, prompt_pos)

        pygame.display.flip()
        clock.tick(6)

        frame_index = (frame_index + 1) % len(win_frames)
        win_text_index = (win_text_index + 1) % len(you_win_frames)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN:
                running = False

    pygame.mixer.music.stop()
    call_return_callback()


def show_lose_screen(screen, loser_name):
    pygame.init()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 36)

    lose_folders = {
        "Cammy": "Character 3",
        "Junli": "Character 1",
        "Kay": "Character 2",
        "Guile": "Character 4"
    }
    lose_folder = f"D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/characters/{lose_folders[loser_name]}/lose"
    lose_frames = load_win_animation(lose_folder)
    you_lose_frames = load_you_lose_frames()

    lose_frame_index = 0
    lose_text_index = 0

    play_victory_music("D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/music/lose_sound.wav")

    prompt_text = font.render("Press any key to retry the level", True, (255, 255, 255))
    prompt_pos = (
        SCREEN_WIDTH // 2 - prompt_text.get_width() // 2,
        SCREEN_HEIGHT - 100
    )

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(you_lose_frames[lose_text_index], (SCREEN_WIDTH // 2 - 350, 40))
        screen.blit(lose_frames[lose_frame_index], (
            SCREEN_WIDTH // 2 - lose_frames[lose_frame_index].get_width() // 2,
            SCREEN_HEIGHT // 2 - lose_frames[lose_frame_index].get_height() // 2 + 40
        ))
        screen.blit(prompt_text, prompt_pos)

        pygame.display.flip()
        clock.tick(6)

        lose_frame_index = (lose_frame_index + 1) % len(lose_frames)
        lose_text_index = (lose_text_index + 1) % len(you_lose_frames)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()
            elif event.type == pygame.KEYDOWN:
                running = False

    pygame.mixer.music.stop()
    call_return_callback()
