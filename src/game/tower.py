import pygame
from game.config import *
from game.projectile import Projectile

class Tower(pygame.sprite.Sprite):
    def __init__(self, gx, gy, t_type, level):
        super().__init__()
        self.gx, self.gy = gx, gy
        self.level = level
        self.stats = TOWER_TYPES[t_type]
        self.type = t_type
        self.cooldown = 0

        self.image = pygame.Surface((TILE_SIZE-20, TILE_SIZE-20))
        self.image.fill(self.stats["color"])
        self.rect = self.image.get_rect(
            center=(gx*TILE_SIZE+TILE_SIZE//2, gy*TILE_SIZE+TILE_SIZE//2)
        )

    def update(self, enemies, projectiles):
        if self.cooldown > 0:
            self.cooldown -= 1
            return
        for e in enemies:
            if pygame.math.Vector2(self.rect.center).distance_to(e.rect.center) < self.stats["range"]:
                projectiles.add(Projectile(self.rect.center, e, self.type))
                self.level.sound.shoot.play()
                self.cooldown = self.stats["cooldown"]
                break
