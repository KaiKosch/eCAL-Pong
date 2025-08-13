import pygame
import time
from typing import Tuple

class PowerUp:
    def __init__(self, target: str, effect_duration: float = 5.0):
        self.width = 5
        self.height = 50
        self.rect = pygame.Rect(400, 300, self.width, self.height)  # middle
        self.active = False
        self.activation_time = 0
        self.effect_duration = effect_duration
        self.target = target  # "left" or "right"

        # movement speed
        self.velocity_x = -2 if target == "left" else 2

    def move(self):
        if not self.active:
            self.rect.x += self.velocity_x

    def check_collision(self, paddle_rect):
        if not self.active and self.rect.colliderect(paddle_rect):
            self.active = True
            self.activation_time = time.time()
            self.rect = pygame.Rect(-100, -100, 0, 0)  # hide
            return True
        return False

    def is_expired(self):
        return self.active and (time.time() - self.activation_time > self.effect_duration)

    def reset(self):
        self.rect = pygame.Rect(400, 300, self.width, self.height)
        self.active = False
        self.activation_time = 0
