import pygame
import os
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class Stage:
    def __init__(self, stage_name):
        pygame.mixer.init()  # Ensure mixer is initialized

        stage_folders = {
            "Street of Art": "dojo",
            "Champion Ring": "championship",
            "Dragon Temple": "dragon"
        }
        music_paths = {
            "Street of Art": "D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/music/Crowd_Cheering_Stadium.wav",
            "Champion Ring": "D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/music/Crowd_Cheering_Stadium.wav",
            "Dragon Temple": "D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/music/temple.wav"
        }

        folder = stage_folders.get(stage_name, "dojo")
        self.path = f"D:/IMAGINE SPECIAL EFFECT ASSIGNMENT/assets/stages/{folder}"
        self.frames = self.load_frames()
        self.index = 0
        self.timer = 0

        # Load and play music
        self.music_path = music_paths.get(stage_name)
        if self.music_path:
            pygame.mixer.music.load(self.music_path)
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1)  # -1 = loop forever

    def load_frames(self):
        return [
            pygame.transform.scale(
                pygame.image.load(os.path.join(self.path, f"tile{str(i).zfill(3)}.png")),
                (SCREEN_WIDTH, SCREEN_HEIGHT)
            )
            for i in range(8)
        ]

    def update(self, speed=5):
        self.timer += 1
        if self.timer >= speed:
            self.index = (self.index + 1) % len(self.frames)
            self.timer = 0

    def draw(self, screen, opacity=100):
        frame = self.frames[self.index].copy().convert_alpha()

        # Simulate blur by scaling down and back up
        small = pygame.transform.smoothscale(frame, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        blur_frame = pygame.transform.smoothscale(small, (SCREEN_WIDTH, SCREEN_HEIGHT))

        if opacity < 255:
            blur_frame.set_alpha(opacity)
        screen.blit(blur_frame, (0, 0))

        # Add translucent black overlay to dim
        dark_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
        dark_overlay.fill((0, 0, 0, 75))  # Adjust alpha for darkness
        screen.blit(dark_overlay, (0, 0))
