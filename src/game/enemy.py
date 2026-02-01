import pygame
import math
from game.config import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, waypoints, e_type, level):
        super().__init__()
        s = ENEMY_TYPES[e_type]

        self.image = pygame.Surface((36,36), pygame.SRCALPHA)
        self.base_color = s["color"]
        pygame.draw.circle(self.image, self.base_color, (18,18), 18)
        self.rect = self.image.get_rect(center=waypoints[0])

        self.waypoints = waypoints
        self.target_idx = 1

        self.hp = s["hp"]
        self.max_hp = s["hp"]
        self.reward = s["reward"]
        self.base_damage = s["dmg"]

        self.orig_speed = s["speed"]
        self.speed = self.orig_speed

        self.fire_timer = 0
        self.freeze_timer = 0
        self.reached_end = False
        self.level = level
        
        self.pos_x = float(self.rect.centerx)
        self.pos_y = float(self.rect.centery)

    def update(self):
        # --- FIRE DOT ---
        if self.fire_timer > 0:
            self.hp -= 0.1
            self.fire_timer -= 1

        # --- FREEZE ---
        if self.freeze_timer > 0:
            self.speed = self.orig_speed * 0.5
            self.freeze_timer -= 1
        else:
            self.speed = min(self.orig_speed, self.speed + 0.02)

        # --- MOVE ---
        target = self.waypoints[self.target_idx]
        dx = target[0] - self.pos_x
        dy = target[1] - self.pos_y
        dist = math.hypot(dx, dy)

        if dist < self.speed:
            self.target_idx += 1
            if self.target_idx >= len(self.waypoints):
                self.reached_end = True
                self.level.base_hp -= self.base_damage
                self.level.sound.base_hit.play()
                self.kill()
        else:
            self.pos_x += (dx/dist) * self.speed
            self.pos_y += (dy/dist) * self.speed
            self.rect.centerx = int(self.pos_x)
            self.rect.centery = int(self.pos_y)

        # --- COLOR UPDATE ---
        color = self.base_color
        if self.freeze_timer > 0:
            color = CYAN
        elif self.fire_timer > 0:
            color = ORANGE

        self.image.fill((0,0,0,0))
        pygame.draw.circle(self.image, color, (18,18), 18)

    def draw_hp_bar(self, screen):
        if self.hp <= 0:
            return
        ratio = max(0, self.hp) / self.max_hp
        pygame.draw.rect(screen, RED,
                         (self.rect.centerx-15, self.rect.top-10, 30, 4))
        pygame.draw.rect(screen, GREEN,
                         (self.rect.centerx-15, self.rect.top-10, 30*ratio, 4))
