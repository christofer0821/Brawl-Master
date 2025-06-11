import pygame
import sys
import os
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from scenes.character_select import character_select, character_select_dual
from scenes.stage_select import stage_select
from modes.pvp_mode import run_pvp_battle
from scenes.result_screen import set_return_callback
from modes.story_mode import run_story_mode

# === INIT ===
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawl Masters")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 36)

# === Music ===
main_menu_music = "D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/music/Main_Menu_Theme.wav"
pygame.mixer.music.load(main_menu_music)
pygame.mixer.music.play(-1)

# === Load background animation (main menu) ===
bg_folder = "assets/Background/Main Menu"
bg_frames = [pygame.transform.scale(pygame.image.load(os.path.join(bg_folder, f"tile00{i}.png")).convert(), (SCREEN_WIDTH, SCREEN_HEIGHT)) for i in range(8)]
bg_index, bg_timer = 0, 0

# === Load animated logo (main menu) ===
logo_folder = "assets/Logo"
logo_frames = [pygame.transform.scale(pygame.image.load(os.path.join(logo_folder, f"tile{str(i).zfill(3)}.png")).convert_alpha(), (800, 300)) for i in range(25)]
logo_index, logo_timer = 0, 0

# === Load button images ===
button_images = {
    "Start": pygame.image.load("assets/Button/play_button.png"),
    "Option": pygame.image.load("assets/Button/option_button.png"),
    "Exit": pygame.image.load("assets/Button/exit_button.png")
}
BUTTON_WIDTH, BUTTON_HEIGHT = 330, 100
HOVER_WIDTH, HOVER_HEIGHT = 370, 110
for key in button_images:
    button_images[key] = pygame.transform.scale(button_images[key], (BUTTON_WIDTH, BUTTON_HEIGHT))

# === Slide transition effect ===
def slide_left_transition(next_scene_func):
    transition_surface = screen.copy()
    for offset in range(0, SCREEN_WIDTH + 1, 40):
        screen.fill((0, 0, 0))
        screen.blit(transition_surface, (-offset, 0))
        pygame.display.update()
        clock.tick(FPS)
    next_scene_func()

def show_tutorial():
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))
    fade_surface.set_alpha(0)

    tutorial_font = pygame.font.SysFont("Arial", 40)
    lines = [
        "Player 1 Controls:",
        "Jab: H | Kick: J | Special: K | Block: L",
        "Crouch: S | Jump: W | Move: A / D",
        "Jump Forward: W + A or W + D",
        "",
        "Player 2 Controls:",
        "Jab: 1 | Kick: 2 | Special: 3 | Block: 4",
        "Crouch: ↓ | Jump: ↑ | Move: ← / →",
        "Jump Forward: ← + ↑ or → + ↑",
        "",
        "Press any key or click to go back."
    ]

    rendered_lines = [tutorial_font.render(line, True, (255, 255, 255)) for line in lines]
    total_height = len(rendered_lines) * 35
    start_y = (SCREEN_HEIGHT - total_height) // 2

    # === Fade-in
    for alpha in range(0, 200, 10):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(20)

    # === Display tutorial
    running = True
    while running:
        screen.blit(fade_surface, (0, 0))
        for i, rendered in enumerate(rendered_lines):
            text_rect = rendered.get_rect(center=(SCREEN_WIDTH // 2, start_y + i * 35))
            screen.blit(rendered, text_rect)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                running = False

    # === Fade-out
    for alpha in range(200, 0, -10):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(20)


# === Main Menu ===
def main_menu():
    global bg_index, bg_timer, logo_index, logo_timer
    buttons = ["Start", "Option", "Exit"]

    while True:
        bg_timer += 1
        if bg_timer >= 5:
            bg_index = (bg_index + 1) % len(bg_frames)
            bg_timer = 0
        screen.blit(bg_frames[bg_index], (0, 0))

        logo_timer += 1
        if logo_timer >= 3:
            logo_index = (logo_index + 1) % len(logo_frames)
            logo_timer = 0
        screen.blit(logo_frames[logo_index], (SCREEN_WIDTH // 2 - 400, -20))

        mouse_pos = pygame.mouse.get_pos()
        button_rects = []
        for i, label in enumerate(buttons):
            img = button_images[label]
            y = 300 + i * 110
            rect = img.get_rect(center=(SCREEN_WIDTH // 2, y))
            is_hovered = rect.collidepoint(mouse_pos)
            if is_hovered:
                img = pygame.transform.scale(img, (HOVER_WIDTH, HOVER_HEIGHT))
                rect = img.get_rect(center=(SCREEN_WIDTH // 2, y))
            screen.blit(img, rect)
            button_rects.append((rect, label))

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, label in button_rects:
                    if rect.collidepoint(mouse_pos):
                        if label == "Start":
                            return slide_left_transition(mode_menu)
                        elif label == "Option":
                            show_tutorial()
                        elif label == "Exit":
                            pygame.quit(); sys.exit()

# === Mode Menu ===
def mode_menu():
    # ✅ Ensure music is playing when re-entering mode menu
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(main_menu_music)
        pygame.mixer.music.play(-1)

    # === Load Mode Buttons (including BACK) ===
    mode_buttons = {
        "Story Mode": pygame.image.load("assets/Button/story_button.png"),
        "PVP Mode": pygame.image.load("assets/Button/pvp_button.png"),
        "Back": pygame.image.load("D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/Button/back_button.png")
    }

    BUTTON_WIDTH, BUTTON_HEIGHT = 320, 200
    HOVER_WIDTH, HOVER_HEIGHT = 360, 220
    for key in mode_buttons:
        mode_buttons[key] = pygame.transform.scale(mode_buttons[key], (BUTTON_WIDTH, BUTTON_HEIGHT))

    # === Load Mode Logo Animation ===
    mode_logo_folder = "assets/Logo 2"
    mode_logo_frames = [
        pygame.transform.scale(
            pygame.image.load(os.path.join(mode_logo_folder, f"tile{str(i).zfill(3)}.png")).convert_alpha(),
            (700, 180)
        )
        for i in range(25)
    ]
    mode_logo_index, mode_logo_timer = 0, 0
    options = list(mode_buttons.keys())

    while True:
        screen.fill((10, 10, 25))

        # === Animated Logo ===
        mode_logo_timer += 1
        if mode_logo_timer >= 4:
            mode_logo_index = (mode_logo_index + 1) % len(mode_logo_frames)
            mode_logo_timer = 0
        screen.blit(mode_logo_frames[mode_logo_index], (SCREEN_WIDTH // 2 - 350, 60))

        # === Render Buttons ===
        mouse_pos = pygame.mouse.get_pos()
        button_rects = []
        for i, label in enumerate(options):
            base_img = mode_buttons[label]
            y = 320 + i * 140
            rect = base_img.get_rect(center=(SCREEN_WIDTH // 2, y))
            is_hovered = rect.collidepoint(mouse_pos)

            if is_hovered:
                img = pygame.transform.scale(base_img, (HOVER_WIDTH, HOVER_HEIGHT))
                rect = img.get_rect(center=(SCREEN_WIDTH // 2, y))
            else:
                img = base_img

            screen.blit(img, rect)
            button_rects.append((rect, label))

        pygame.display.flip()
        clock.tick(FPS)

        # === Button Logic ===
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for rect, label in button_rects:
                    if rect.collidepoint(mouse_pos):
                        if label == "PVP Mode":
                            char_select_music = "D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/music/Character_Select_Theme.wav"
                            pygame.mixer.music.load(char_select_music)
                            pygame.mixer.music.play(-1)

                            p1 = character_select(screen, font, prompt="Player 1 - Choose Character", preview_side="left")
                            p2 = character_select_dual(screen, font, p1_selected_name=p1, prompt="Player 2 - Choose Character")
                            stage = stage_select(screen, font)

                            pygame.mixer.music.stop()
                            run_pvp_battle(p1, p2, stage)

                            # 🔁 Resume main menu music after PvP ends
                            pygame.mixer.music.load(main_menu_music)
                            pygame.mixer.music.play(-1)

                        elif label == "Story Mode":
                            pygame.mixer.music.stop()
                            run_story_mode()
                            pygame.mixer.music.load(main_menu_music)
                            pygame.mixer.music.play(-1)

                        elif label == "Back":
                            return slide_left_transition(main_menu)


# === Run the Game ===
if __name__ == "__main__":
    set_return_callback(lambda: slide_left_transition(mode_menu))
    main_menu()
