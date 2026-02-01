import pygame
import math
from game.config import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, target, t_type):
        super().__init__()
        self.target = target
        self.type = t_type
        self.speed = 10

        self.image = pygame.Surface((12,12), pygame.SRCALPHA)
        pygame.draw.circle(self.image, TOWER_TYPES[t_type]["color"], (6,6), 6)
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        if not self.target.alive():
            self.kill()
            return

        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)

        if dist < self.speed:
            dmg = 8
            if self.type == "fire":
                self.target.fire_timer = 300
            elif self.type == "freeze":
                dmg = 4
                self.target.freeze_timer = 120

            self.target.hp -= dmg
            self.target.level.sound.hit.play()
            self.kill()
        else:
            self.rect.centerx += (dx / dist) * self.speed
            self.rect.centery += (dy / dist) * self.speed
