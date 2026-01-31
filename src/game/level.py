import pygame
import time
import math
from game.config import *

class Level:
    def __init__(self, screen):
        self.screen = screen
        self.money = STARTING_MONEY
        self.base_hp = BASE_HP
        self.grid_data = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.path_coords = [(0, 2), (4, 2), (4, 6), (10, 6), (10, 1), (13, 1)]
        self.waypoints = [(c[0] * TILE_SIZE + TILE_SIZE//2, c[1] * TILE_SIZE + TILE_SIZE//2) for c in self.path_coords]
        
        for i in range(len(self.path_coords)-1):
            p1, p2 = self.path_coords[i], self.path_coords[i+1]
            for x in range(min(p1[0], p2[0]), max(p1[0], p2[0]) + 1):
                for y in range(min(p1[1], p2[1]), max(p1[1], p2[1]) + 1):
                    if y < GRID_HEIGHT and x < GRID_WIDTH: self.grid_data[y][x] = 1

        self.towers = []
        self.enemies = []
        self.projectiles = []
        self.show_grid = True
        self.selected_type = "basic"
        self.wave_num = 1
        self.spawn_queue = []
        self.spawn_timer = 0
        self.in_wave = False
        self.show_info = False
        
        self.ui_panel_x = WIDTH - 200
        self.shop_buttons = {t: pygame.Rect(self.ui_panel_x+20, 160+i*60, 160, 45) for i, t in enumerate(TOWER_TYPES.keys())}
        self.grid_toggle_rect = pygame.Rect(self.ui_panel_x + 20, HEIGHT - 110, 160, 45)
        self.info_btn_rect = pygame.Rect(self.ui_panel_x + 20, HEIGHT - 55, 160, 45)
        self.start_wave_rect = pygame.Rect(self.ui_panel_x + 20, 430, 160, 50)
        
        self.info_rect = pygame.Rect(100, 100, 800, 500)
        self.info_close_rect = pygame.Rect(860, 110, 30, 30)

    def prepare_wave(self):
        self.spawn_queue = []
        w = self.wave_num
        s_count = 10 + ((w-1) % 5) * 5
        for _ in range(s_count): self.spawn_queue.append("soldier")
        if w >= 5:
            v_count = 2 + ((w-5) % 5) if w < 10 else 2 + ((w-10) % 5)
            if w == 15: v_count = 2
            for _ in range(v_count): self.spawn_queue.append("vehicle")
        if w >= 10:
            t_count = 1 + ((w-10) % 5)
            if w == 15: t_count = 1
            for _ in range(t_count): self.spawn_queue.append("tank")
        if w == 15: self.spawn_queue.append("boss")
        self.in_wave = True

    def handle_click(self, mouse_pos):
        if self.show_info:
            if self.info_close_rect.collidepoint(mouse_pos):
                self.show_info = False
            return
        if self.info_btn_rect.collidepoint(mouse_pos):
            self.show_info = True
            return
        for t_name, rect in self.shop_buttons.items():
            if rect.collidepoint(mouse_pos): self.selected_type = t_name; return
        if self.grid_toggle_rect.collidepoint(mouse_pos): self.show_grid = not self.show_grid; return
        if self.start_wave_rect.collidepoint(mouse_pos) and not self.in_wave: self.prepare_wave(); return
        gx, gy = mouse_pos[0] // TILE_SIZE, mouse_pos[1] // TILE_SIZE
        if self.can_place_tower(gx, gy):
            self.towers.append(Tower(gx, gy, self.selected_type))
            self.money -= TOWER_TYPES[self.selected_type]["cost"]

    def can_place_tower(self, gx, gy):
        if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
            if self.grid_data[gy][gx] == 0 and self.money >= TOWER_TYPES[self.selected_type]["cost"]:
                return not any(t.gx == gx and t.gy == gy for t in self.towers)
        return False

    def update(self):
        if self.in_wave:
            self.spawn_timer += 1
            if self.spawn_timer > 40 and self.spawn_queue:
                self.enemies.append(Enemy(self.waypoints, self.spawn_queue.pop(0)))
                self.spawn_timer = 0
            if not self.spawn_queue and not self.enemies:
                self.in_wave = False
                self.wave_num += 1
        for e in self.enemies[:]:
            e.update()
            if e.finished:
                self.base_hp -= e.base_damage
                self.enemies.remove(e)
            elif e.hp <= 0:
                self.money += e.reward
                self.enemies.remove(e)
        for t in self.towers:
            shots = t.update(self.enemies)
            for s in shots: self.projectiles.append(s)
        for p in self.projectiles[:]:
            p.update()
            if p.hit: self.projectiles.remove(p)

    def draw(self, mouse_pos):
        gx, gy = mouse_pos[0] // TILE_SIZE, mouse_pos[1] // TILE_SIZE
        for r in range(GRID_HEIGHT):
            for c in range(GRID_WIDTH):
                rect = pygame.Rect(c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if self.show_grid:
                    color = (30,30,30) if self.grid_data[r][c] == 1 else (15,15,15)
                    if c == gx and r == gy: color = WHITE if self.can_place_tower(c,r) else RED
                    pygame.draw.rect(self.screen, color, rect)
                    pygame.draw.rect(self.screen, (40,40,40), rect, 1)
                elif self.grid_data[r][c] == 1: pygame.draw.rect(self.screen, (25,25,25), rect)
        pygame.draw.rect(self.screen, GREEN, (self.path_coords[-1][0]*TILE_SIZE, self.path_coords[-1][1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))
        for t in self.towers: t.draw(self.screen)
        for e in self.enemies: e.draw(self.screen)
        for p in self.projectiles: p.draw(self.screen)
        self.draw_ui()
        if self.show_info: self.draw_info_screen()

    def draw_ui(self):
        pygame.draw.rect(self.screen, (20,20,20), (self.ui_panel_x, 0, 200, HEIGHT))
        f = pygame.font.SysFont(None, 28)
        self.screen.blit(f.render(f"Gold: {self.money}$", True, GOLD), (self.ui_panel_x+20, 20))
        self.screen.blit(f.render(f"HP: {self.base_hp}", True, RED), (self.ui_panel_x+20, 50))
        self.screen.blit(f.render(f"Wave: {self.wave_num}", True, WHITE), (self.ui_panel_x+20, 80))
        rem = len(self.spawn_queue) + len(self.enemies)
        self.screen.blit(f.render(f"Enemies: {rem}", True, CYAN), (self.ui_panel_x+20, 110))
        fs = pygame.font.SysFont(None, 24)
        for t_name, rect in self.shop_buttons.items():
            pygame.draw.rect(self.screen, TOWER_TYPES[t_name]["color"], rect)
            if self.selected_type == t_name: pygame.draw.rect(self.screen, WHITE, rect.inflate(4,4), 2)
            self.screen.blit(fs.render(f"{t_name.upper()} {TOWER_TYPES[t_name]['cost']}$", True, BLACK), (rect.x+10, rect.y+12))
        if not self.in_wave:
            pygame.draw.rect(self.screen, GREEN, self.start_wave_rect)
            self.screen.blit(fs.render("START WAVE", True, BLACK), (self.start_wave_rect.x+25, self.start_wave_rect.y+15))
        else:
            pygame.draw.rect(self.screen, (40,40,40), self.start_wave_rect)
            self.screen.blit(fs.render("IN PROGRESS", True, WHITE), (self.start_wave_rect.x+25, self.start_wave_rect.y+15))
        pygame.draw.rect(self.screen, (60,60,60), self.grid_toggle_rect)
        self.screen.blit(fs.render("TOGGLE GRID", True, WHITE), (self.grid_toggle_rect.x+20, self.grid_toggle_rect.y+12))
        pygame.draw.rect(self.screen, BLUE, self.info_btn_rect)
        self.screen.blit(fs.render("INFO / HELP", True, WHITE), (self.info_btn_rect.x+30, self.info_btn_rect.y+12))

    def draw_info_screen(self):
        surf = pygame.Surface((self.info_rect.width, self.info_rect.height))
        surf.set_alpha(240)
        surf.fill((10,10,10))
        self.screen.blit(surf, (self.info_rect.x, self.info_rect.y))
        pygame.draw.rect(self.screen, WHITE, self.info_rect, 2)
        pygame.draw.rect(self.screen, RED, self.info_close_rect)
        fc = pygame.font.SysFont(None, 30, bold=True)
        self.screen.blit(fc.render("X", True, WHITE), (self.info_close_rect.x+8, self.info_close_rect.y+5))
        fi = pygame.font.SysFont(None, 26)
        txt = [
            "TOWERS:", "B - Basic: Balanced", "D - Double: Fast", "F - Fire: DOT damage", "S - Slow: 50% Speed", 
            "", "ENEMIES:", "Soldier: 20hp / 2.5spd", "Vehicle: 120hp / 3.5spd", "Tank: 500hp / 1.2spd", "Boss: 3500hp / 0.6spd"
        ]
        for i, l in enumerate(txt): self.screen.blit(fi.render(l, True, WHITE), (130, 150+i*30))

class Enemy:
    def __init__(self, waypoints, e_type):
        self.waypoints = waypoints
        self.target_idx = 1
        self.x, self.y = waypoints[0]
        self.finished = False
        s = ENEMY_TYPES[e_type]
        self.orig_speed = s["speed"]
        self.speed = self.orig_speed
        self.hp = s["hp"]
        self.max_hp = self.hp
        self.reward = s["reward"]
        self.base_damage = s["dmg"]
        self.color = s["color"]
        self.fire_timer = 0
        self.freeze_timer = 0

    def update(self):
        if self.fire_timer > 0: self.hp -= 0.1; self.fire_timer -= 1
        if self.freeze_timer > 0: self.speed = self.orig_speed * 0.5; self.freeze_timer -= 1
        else:
            if self.speed < self.orig_speed: self.speed += 0.02
        t = self.waypoints[self.target_idx]
        dx, dy = t[0] - self.x, t[1] - self.y
        dist = math.hypot(dx, dy)
        if dist < self.speed:
            self.target_idx += 1
            if self.target_idx >= len(self.waypoints): self.finished = True
        else:
            self.x += (dx/dist) * self.speed
            self.y += (dy/dist) * self.speed

    def draw(self, screen):
        c = CYAN if self.freeze_timer > 0 else (ORANGE if self.fire_timer > 0 else self.color)
        pygame.draw.circle(screen, c, (int(self.x), int(self.y)), 18)
        pygame.draw.rect(screen, RED, (self.x-15, self.y-25, 30, 4))
        pygame.draw.rect(screen, GREEN, (self.x-15, self.y-25, 30*(max(0, self.hp)/self.max_hp), 4))

class Tower:
    def __init__(self, gx, gy, t_type):
        self.gx, self.gy, self.type = gx, gy, t_type
        self.stats = TOWER_TYPES[t_type]
        self.x, self.y = gx*TILE_SIZE + TILE_SIZE//2, gy*TILE_SIZE + TILE_SIZE//2
        self.cooldown = 0

    def update(self, enemies):
        if self.cooldown > 0: self.cooldown -= 1
        if self.cooldown == 0:
            for e in enemies:
                if math.hypot(e.x - self.x, e.y - self.y) < self.stats["range"]:
                    self.cooldown = self.stats["cooldown"]
                    return [Projectile(self.x, self.y, e, self.type)]
        return []

    def draw(self, screen):
        pygame.draw.rect(screen, self.stats["color"], (self.gx*TILE_SIZE+10, self.gy*TILE_SIZE+10, TILE_SIZE-20, TILE_SIZE-20))

class Projectile:
    def __init__(self, x, y, target, t_type):
        self.x, self.y, self.target, self.type = x, y, target, t_type
        self.speed, self.hit = 10, False

    def update(self):
        dx, dy = self.target.x - self.x, self.target.y - self.y
        dist = math.hypot(dx, dy)
        if dist < self.speed:
            self.apply()
            self.hit = True
        else:
            self.x += (dx/dist) * self.speed
            self.y += (dy/dist) * self.speed

    def apply(self):
        d = 8
        if self.type == "fire": self.target.fire_timer = 300
        elif self.type == "freeze": d = 4; self.target.freeze_timer = 120
        self.target.hp -= d

    def draw(self, screen):
        pygame.draw.circle(screen, TOWER_TYPES[self.type]["color"], (int(self.x), int(self.y)), 6)