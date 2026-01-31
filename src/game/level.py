import pygame
import time
import math
from game.config import *


# ===================== LEVEL =====================

class Level:
    def __init__(self, screen):
        self.screen = screen
        self.money = STARTING_MONEY
        self.base_hp = BASE_HP

        self.grid_data = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.path_coords = [(0, 2), (4, 2), (4, 6), (10, 6), (10, 1), (13, 1)]
        self.waypoints = [(c[0]*TILE_SIZE+TILE_SIZE//2,
                           c[1]*TILE_SIZE+TILE_SIZE//2) for c in self.path_coords]

        for i in range(len(self.path_coords)-1):
            p1, p2 = self.path_coords[i], self.path_coords[i+1]
            for x in range(min(p1[0], p2[0]), max(p1[0], p2[0])+1):
                for y in range(min(p1[1], p2[1]), max(p1[1], p2[1])+1):
                    if y < GRID_HEIGHT and x < GRID_WIDTH:
                        self.grid_data[y][x] = 1

        # SPRITE GROUPS
        self.towers = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

        self.show_grid = True
        self.selected_type = "basic"
        self.wave_num = 1
        self.spawn_queue = []
        self.spawn_timer = 0
        self.in_wave = False
        self.show_info = False

        self.ui_panel_x = WIDTH - 200
        self.shop_buttons = {t: pygame.Rect(self.ui_panel_x+20, 160+i*60, 160, 45)
                             for i, t in enumerate(TOWER_TYPES.keys())}
        self.grid_toggle_rect = pygame.Rect(self.ui_panel_x+20, HEIGHT-110, 160, 45)
        self.info_btn_rect = pygame.Rect(self.ui_panel_x+20, HEIGHT-55, 160, 45)
        self.start_wave_rect = pygame.Rect(self.ui_panel_x+20, 430, 160, 50)

        self.info_rect = pygame.Rect(100, 100, 800, 500)
        self.info_close_rect = pygame.Rect(860, 110, 30, 30)

    # ---------------- WAVE ----------------

    def prepare_wave(self):
        self.spawn_queue = []
        w = self.wave_num

        for _ in range(10 + ((w-1) % 5) * 5):
            self.spawn_queue.append("soldier")

        if w >= 5:
            for _ in range(2 + ((w-5) % 5)):
                self.spawn_queue.append("vehicle")

        if w >= 10:
            for _ in range(1 + ((w-10) % 5)):
                self.spawn_queue.append("tank")

        if w == 15:
            self.spawn_queue.append("boss")

        self.in_wave = True

    # ---------------- INPUT ----------------

    def handle_click(self, mouse_pos):
        if self.show_info:
            if self.info_close_rect.collidepoint(mouse_pos):
                self.show_info = False
            return

        if self.info_btn_rect.collidepoint(mouse_pos):
            self.show_info = True
            return

        for t_name, rect in self.shop_buttons.items():
            if rect.collidepoint(mouse_pos):
                self.selected_type = t_name
                return

        if self.grid_toggle_rect.collidepoint(mouse_pos):
            self.show_grid = not self.show_grid
            return

        if self.start_wave_rect.collidepoint(mouse_pos) and not self.in_wave:
            self.prepare_wave()
            return

        gx, gy = mouse_pos[0] // TILE_SIZE, mouse_pos[1] // TILE_SIZE
        if self.can_place_tower(gx, gy):
            self.towers.add(Tower(gx, gy, self.selected_type))
            self.money -= TOWER_TYPES[self.selected_type]["cost"]

    def can_place_tower(self, gx, gy):
        if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
            if self.grid_data[gy][gx] == 0:
                if self.money >= TOWER_TYPES[self.selected_type]["cost"]:
                    return not any(t.gx == gx and t.gy == gy for t in self.towers)
        return False

    # ---------------- UPDATE ----------------

    def update(self):
        if self.in_wave:
            self.spawn_timer += 1
            if self.spawn_timer > 40 and self.spawn_queue:
                self.enemies.add(
                    Enemy(self.waypoints, self.spawn_queue.pop(0),self)
                )
                self.spawn_timer = 0

            if not self.spawn_queue and not self.enemies:
                self.in_wave = False
                self.wave_num += 1

        self.enemies.update()
        self.projectiles.update()

        for t in self.towers:
            t.update(self.enemies, self.projectiles)

        for e in self.enemies.copy():
            if e.hp <= 0:
                self.money += e.reward
                e.kill()

    # ---------------- DRAW ----------------

    def draw(self, mouse_pos):
        gx, gy = mouse_pos[0] // TILE_SIZE, mouse_pos[1] // TILE_SIZE

        for r in range(GRID_HEIGHT):
            for c in range(GRID_WIDTH):
                rect = pygame.Rect(c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if self.show_grid:
                    color = (30,30,30) if self.grid_data[r][c] == 1 else (15,15,15)
                    if (c, r) == (gx, gy):
                        color = WHITE if self.can_place_tower(c, r) else RED
                    pygame.draw.rect(self.screen, color, rect)
                    pygame.draw.rect(self.screen, (40,40,40), rect, 1)
                elif self.grid_data[r][c] == 1:
                    pygame.draw.rect(self.screen, (25,25,25), rect)

        pygame.draw.rect(
            self.screen, GREEN,
            (self.path_coords[-1][0]*TILE_SIZE,
             self.path_coords[-1][1]*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        )

        self.towers.draw(self.screen)
        self.enemies.draw(self.screen)
        for e in self.enemies:
            e.draw_hp_bar(self.screen)
        self.projectiles.draw(self.screen)

        self.draw_ui()
        if self.show_info:
            self.draw_info_screen()

    # ---------------- UI ----------------

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
            if self.selected_type == t_name:
                pygame.draw.rect(self.screen, WHITE, rect.inflate(4,4), 2)
            self.screen.blit(
                fs.render(f"{t_name.upper()} {TOWER_TYPES[t_name]['cost']}$", True, BLACK),
                (rect.x+10, rect.y+12)
            )

        if not self.in_wave:
            pygame.draw.rect(self.screen, GREEN, self.start_wave_rect)
            self.screen.blit(fs.render("START WAVE", True, BLACK),
                             (self.start_wave_rect.x+25, self.start_wave_rect.y+15))
        else:
            pygame.draw.rect(self.screen, (40,40,40), self.start_wave_rect)
            self.screen.blit(fs.render("IN PROGRESS", True, WHITE),
                             (self.start_wave_rect.x+25, self.start_wave_rect.y+15))

        pygame.draw.rect(self.screen, (60,60,60), self.grid_toggle_rect)
        self.screen.blit(fs.render("TOGGLE GRID", True, WHITE),
                         (self.grid_toggle_rect.x+20, self.grid_toggle_rect.y+12))

        pygame.draw.rect(self.screen, BLUE, self.info_btn_rect)
        self.screen.blit(fs.render("INFO / HELP", True, WHITE),
                         (self.info_btn_rect.x+30, self.info_btn_rect.y+12))

    def draw_info_screen(self):
        surf = pygame.Surface(self.info_rect.size)
        surf.set_alpha(240)
        surf.fill((10,10,10))
        self.screen.blit(surf, self.info_rect.topleft)
        pygame.draw.rect(self.screen, WHITE, self.info_rect, 2)
        pygame.draw.rect(self.screen, RED, self.info_close_rect)

        fc = pygame.font.SysFont(None, 30, bold=True)
        self.screen.blit(fc.render("X", True, WHITE),
                         (self.info_close_rect.x+8, self.info_close_rect.y+5))

        fi = pygame.font.SysFont(None, 26)
        txt = [
            "TOWERS:", "B - Basic: Balanced", "D - Double: Fast",
            "F - Fire: DOT damage", "S - Slow: 50% Speed",
            "", "ENEMIES:", "Soldier: 20hp / 2.5spd",
            "Vehicle: 120hp / 3.5spd", "Tank: 500hp / 1.2spd",
            "Boss: 3500hp / 0.6spd"
        ]
        for i, l in enumerate(txt):
            self.screen.blit(fi.render(l, True, WHITE), (130, 150+i*30))


# ===================== ENEMY =====================

class Enemy(pygame.sprite.Sprite):
    def __init__(self, waypoints, e_type,level):
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
        dx = target[0] - self.rect.centerx
        dy = target[1] - self.rect.centery
        dist = math.hypot(dx, dy)

        if dist < self.speed:
            self.target_idx += 1
            if self.target_idx >= len(self.waypoints):
                self.reached_end = True
                self.level.base_hp -= self.base_damage
                self.kill()
                
        else:
            self.rect.centerx += (dx/dist) * self.speed
            self.rect.centery += (dy/dist) * self.speed

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

# ===================== TOWER =====================

class Tower(pygame.sprite.Sprite):
    def __init__(self, gx, gy, t_type):
        super().__init__()
        self.gx, self.gy = gx, gy
        self.stats = TOWER_TYPES[t_type]
        self.type = t_type

        self.image = pygame.Surface((TILE_SIZE-20, TILE_SIZE-20))
        self.image.fill(self.stats["color"])
        self.rect = self.image.get_rect(
            center=(gx*TILE_SIZE+TILE_SIZE//2,
                    gy*TILE_SIZE+TILE_SIZE//2)
        )

        self.cooldown = 0

    def update(self, enemies, projectiles):
        if self.cooldown > 0:
            self.cooldown -= 1
            return

        for e in enemies:
            if pygame.math.Vector2(self.rect.center).distance_to(e.rect.center) < self.stats["range"]:
                projectiles.add(Projectile(self.rect.center, e, self.type))
                self.cooldown = self.stats["cooldown"]
                break


# ===================== PROJECTILE =====================

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
            self.kill()
        else:
            self.rect.centerx += (dx / dist) * self.speed
            self.rect.centery += (dy / dist) * self.speed
