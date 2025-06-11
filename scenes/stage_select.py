import pygame
import os
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

# === Stage Info ===
STAGES = [
    {
        "name": "Street of Art",
        "folder": "D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/stages/dojo",
        "tiles": 8,
        "thumb": "D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/stages/dojo/tile000.png"
    },
    {
        "name": "Champion Ring",
        "folder": "D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/stages/championship",
        "tiles": 43,
        "thumb": "D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/stages/championship/tile000.png"
    },
    {
        "name": "Dragon Temple",
        "folder": "D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/stages/dragon",
        "tiles": 8,
        "thumb": "D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/stages/dragon/tile000.png"
    }
]

THUMB_SIZE = (200, 120)


def load_stage_previews():
    previews = {}
    for stage in STAGES:
        frames = []
        for i in range(stage["tiles"]):
            frame_path = os.path.join(stage["folder"], f"tile{str(i).zfill(3)}.png")
            if os.path.exists(frame_path):
                img = pygame.transform.scale(
                    pygame.image.load(frame_path).convert(),
                    (SCREEN_WIDTH, SCREEN_HEIGHT)
                )
                frames.append(img)
        previews[stage["name"]] = frames if frames else [pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))]
    return previews


def load_stage_thumbnails():
    thumbs = {}
    for stage in STAGES:
        img = pygame.image.load(stage["thumb"]).convert()
        img = pygame.transform.scale(img, THUMB_SIZE)
        thumbs[stage["name"]] = img
    return thumbs


def stage_select(screen, font):
    clock = pygame.time.Clock()
    previews = load_stage_previews()
    thumbs = load_stage_thumbnails()
    selected_index = 0
    preview_index = 0
    preview_timer = 0
    confirmed = False

    while not confirmed:
        screen.fill((0, 0, 0))

        # Hover detection
        mouse_pos = pygame.mouse.get_pos()
        hovered_index = None
        thumb_y = 500
        spacing = 80
        start_x = SCREEN_WIDTH // 2 - ((len(STAGES) * (THUMB_SIZE[0] + spacing)) - spacing) // 2

        for i, stage in enumerate(STAGES):
            rect = pygame.Rect(start_x + i * (THUMB_SIZE[0] + spacing), thumb_y, *THUMB_SIZE)
            if rect.collidepoint(mouse_pos):
                hovered_index = i

        # Update preview based on hover or selection
        if hovered_index is not None:
            active_index = hovered_index
        else:
            active_index = selected_index

        stage_name = STAGES[active_index]["name"]
        frames = previews[stage_name]
        if frames:  # Ensure there is at least one frame
            preview_timer += 1
            if preview_timer >= 6:
                preview_index = (preview_index + 1) % len(frames)
                preview_timer = 0
            bg_frame = frames[preview_index % len(frames)].copy()
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.blit(bg_frame, (0, 0))
            overlay.set_alpha(100)  # Adjust this value (0–255) to control opacity
            screen.blit(overlay, (0, 0))

        # Draw thumbnails
        for i, stage in enumerate(STAGES):
            rect = pygame.Rect(start_x + i * (THUMB_SIZE[0] + spacing), thumb_y, *THUMB_SIZE)
            pygame.draw.rect(screen, (20, 20, 20), rect)
            screen.blit(thumbs[stage["name"]], rect.topleft)
            pygame.draw.rect(screen, (255, 255, 0) if i == active_index else (180, 180, 180), rect, 3)

            label = font.render(stage["name"], True, (255, 255, 255))
            screen.blit(label, (rect.centerx - label.get_width() // 2, rect.bottom + 10))

        # Draw title
        title = font.render("Select Stage", True, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 40))

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_index = (selected_index - 1) % len(STAGES)
                elif event.key == pygame.K_RIGHT:
                    selected_index = (selected_index + 1) % len(STAGES)
                elif event.key == pygame.K_RETURN:
                    confirmed = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if hovered_index is not None:
                    selected_index = hovered_index
                    confirmed = True

    return STAGES[selected_index]["name"]