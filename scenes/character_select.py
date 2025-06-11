import pygame
import os
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

CHARACTERS = ["Kay", "Junli", "Cammy","Guile"]
CHARACTER_GRID = [["Kay", "Junli", "Cammy", "Guile"]]

THUMB_SIZE = (120, 120)
PREVIEW_SIZE = (380, 380)

def load_character_assets():
    base_path = "assets/characters/Char Selection"
    data = {}
    for name in CHARACTERS:
        thumb = pygame.image.load(os.path.join(base_path, f"potrait_{name.lower()}.png")).convert_alpha()
        data[name] = pygame.transform.scale(thumb, THUMB_SIZE)
    return data

def load_animated_previews():
    data = {}
    junli_path = "D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/characters/Character 1/Idle"
    kay_path = "D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/characters/Character 2/idle"
    cammy_path = "D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/characters/Character 3/Idle"
    guile_path = "D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/characters/Character 4/idle"

    data["Junli"] = [pygame.transform.scale(pygame.image.load(os.path.join(junli_path, f"tile00{i}.png")).convert_alpha(), PREVIEW_SIZE) for i in range(4)]
    data["Kay"] = [pygame.transform.scale(pygame.image.load(os.path.join(kay_path, f"tile00{i}.png")).convert_alpha(), PREVIEW_SIZE) for i in range(5)]
    data["Cammy"] = [pygame.transform.scale(pygame.image.load(os.path.join(cammy_path, f"tile00{i}.png")).convert_alpha(), PREVIEW_SIZE) for i in range(4)]  # Adjust number of frames as needed
    data["Guile"] = [pygame.transform.scale(pygame.image.load(os.path.join(guile_path, f"tile00{i}.png")).convert_alpha(), PREVIEW_SIZE) for i in range(5)]
    return data


def load_background_frames():
    BG_PATH = "D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/characters/Char Selection/char_selection_bg"
    return [
        pygame.transform.scale(
            pygame.image.load(os.path.join(BG_PATH, f"tile00{i}.png")).convert(), (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        for i in range(8)
    ]

def draw_background(screen, frame_index, bg_frames, alpha=200):
    frame = bg_frames[frame_index].copy()
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert()
    overlay.blit(frame, (0, 0))
    overlay.set_alpha(alpha)
    screen.blit(overlay, (0, 0))

def character_select(screen, font, prompt="Select Character", preview_side="left"):
    clock = pygame.time.Clock()
    thumbs = load_character_assets()
    previews = load_animated_previews()
    bg_frames = load_background_frames()

    selected_row, selected_col = 0, 0
    confirmed = False
    bg_index = 0
    bg_timer = 0
    preview_index = 0
    preview_timer = 0

    while not confirmed:
        bg_timer += 1
        if bg_timer >= 5:
            bg_index = (bg_index + 1) % len(bg_frames)
            bg_timer = 0
        draw_background(screen, bg_index, bg_frames, alpha=50)

        prompt_text = font.render(prompt, True, (255, 255, 255))
        screen.blit(prompt_text, (SCREEN_WIDTH // 2 - prompt_text.get_width() // 2, 80))

        grid_start_x = SCREEN_WIDTH // 2 - (len(CHARACTER_GRID[0]) * (THUMB_SIZE[0] + 30)) // 2
        grid_start_y = 160
        mouse_pos = pygame.mouse.get_pos()
        hovered_char = None

        for row in range(len(CHARACTER_GRID)):
            for col in range(len(CHARACTER_GRID[0])):
                name = CHARACTER_GRID[row][col]
                if not name:
                    continue
                x = grid_start_x + col * (THUMB_SIZE[0] + 30)
                y = grid_start_y + row * (THUMB_SIZE[1] + 30)
                rect = pygame.Rect(x, y, *THUMB_SIZE)
                pygame.draw.rect(screen, (30, 30, 30), rect)
                screen.blit(thumbs[name], rect.topleft)

                if rect.collidepoint(mouse_pos):
                    hovered_char = name
                    selected_row, selected_col = row, col
                    pygame.draw.rect(screen, (255, 255, 0), rect, 4)
                elif row == selected_row and col == selected_col:
                    pygame.draw.rect(screen, (0, 200, 255), rect, 3)

        selected_name = CHARACTER_GRID[selected_row][selected_col]
        if selected_name:
            preview_timer += 1
            if preview_timer >= 10:
                preview_index = (preview_index + 1) % len(previews[selected_name])
                preview_timer = 0
            frame = previews[selected_name][preview_index % len(previews[selected_name])]
            if preview_side == "left":
                screen.blit(frame, (100, 300))
            else:
                screen.blit(frame, (SCREEN_WIDTH - PREVIEW_SIZE[0] - 100, 300))

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    selected_col = (selected_col + 1) % len(CHARACTER_GRID[0])
                elif event.key == pygame.K_LEFT:
                    selected_col = (selected_col - 1) % len(CHARACTER_GRID[0])
                elif event.key == pygame.K_DOWN:
                    selected_row = (selected_row + 1) % len(CHARACTER_GRID)
                elif event.key == pygame.K_UP:
                    selected_row = (selected_row - 1) % len(CHARACTER_GRID)
                elif event.key == pygame.K_RETURN:
                    
                    confirmed = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if hovered_char:
                    
                    return hovered_char

    return CHARACTER_GRID[selected_row][selected_col]

def character_select_dual(screen, font, p1_selected_name, prompt="Player 2 - Choose Character"):
    clock = pygame.time.Clock()
    thumbs = load_character_assets()
    previews = load_animated_previews()
    bg_frames = load_background_frames()

    selected_row, selected_col = 0, 0
    confirmed = False
    bg_index = 0
    bg_timer = 0
    preview_index = 0
    preview_timer = 0

    while not confirmed:
        bg_timer += 1
        if bg_timer >= 5:
            bg_index = (bg_index + 1) % len(bg_frames)
            bg_timer = 0
        draw_background(screen, bg_index, bg_frames, alpha=200)

        prompt_text = font.render(prompt, True, (255, 255, 255))
        screen.blit(prompt_text, (SCREEN_WIDTH // 2 - prompt_text.get_width() // 2, 80))

        grid_start_x = SCREEN_WIDTH // 2 - (len(CHARACTER_GRID[0]) * (THUMB_SIZE[0] + 30)) // 2
        grid_start_y = 160
        mouse_pos = pygame.mouse.get_pos()
        hovered_char = None

        for row in range(len(CHARACTER_GRID)):
            for col in range(len(CHARACTER_GRID[0])):
                name = CHARACTER_GRID[row][col]
                if not name:
                    continue
                x = grid_start_x + col * (THUMB_SIZE[0] + 30)
                y = grid_start_y + row * (THUMB_SIZE[1] + 30)
                rect = pygame.Rect(x, y, *THUMB_SIZE)
                pygame.draw.rect(screen, (30, 30, 30), rect)
                screen.blit(thumbs[name], rect.topleft)

                if rect.collidepoint(mouse_pos):
                    hovered_char = name
                    selected_row, selected_col = row, col
                    pygame.draw.rect(screen, (255, 255, 0), rect, 4)
                elif row == selected_row and col == selected_col:
                    pygame.draw.rect(screen, (0, 200, 255), rect, 3)

        p1_frames = previews[p1_selected_name]
        frame1 = p1_frames[preview_index % len(p1_frames)]
        screen.blit(frame1, (100, 300))

        selected_name = CHARACTER_GRID[selected_row][selected_col]
        if selected_name:
            preview_timer += 1
            if preview_timer >= 10:
                preview_index = (preview_index + 1) % len(previews[selected_name])
                preview_timer = 0
            frame2 = previews[selected_name][preview_index % len(previews[selected_name])]
            flipped_frame = pygame.transform.flip(frame2, True, False)
            screen.blit(flipped_frame, (SCREEN_WIDTH - PREVIEW_SIZE[0] - 100, 300))

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    selected_col = (selected_col + 1) % len(CHARACTER_GRID[0])
                elif event.key == pygame.K_LEFT:
                    selected_col = (selected_col - 1) % len(CHARACTER_GRID[0])
                elif event.key == pygame.K_DOWN:
                    selected_row = (selected_row + 1) % len(CHARACTER_GRID)
                elif event.key == pygame.K_UP:
                    selected_row = (selected_row - 1) % len(CHARACTER_GRID)
                elif event.key == pygame.K_RETURN:
                    
                    confirmed = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if hovered_char:
                    
                    return hovered_char

    return CHARACTER_GRID[selected_row][selected_col]
