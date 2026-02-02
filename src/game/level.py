import pygame
import math
from game.config import *
from game.enemy import Enemy
from game.tower import Tower

class Level:
    def __init__(self, screen, sound):
        self.screen, self.sound = screen, sound
        self.money, self.base_hp = STARTING_MONEY, BASE_HP
        self.game_speed = 1 
        self.won = False
        self.lost = False
        self.need_restart = False

        self.grid_data = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.path_coords = [(0, 2), (4, 2), (4, 6), (10, 6), (10, 1), (13, 1)]
        self.waypoints = [(c[0]*TILE_SIZE+TILE_SIZE//2, c[1]*TILE_SIZE+TILE_SIZE//2) for c in self.path_coords]
        
        for i in range(len(self.path_coords)-1):
            p1, p2 = self.path_coords[i], self.path_coords[i+1]
            for x in range(min(p1[0], p2[0]), max(p1[0], p2[0])+1):
                for y in range(min(p1[1], p2[1]), max(p1[1], p2[1])+1):
                    if y < GRID_HEIGHT and x < GRID_WIDTH: self.grid_data[y][x] = 1
                    
        self.towers, self.enemies, self.projectiles = pygame.sprite.Group(), pygame.sprite.Group(), pygame.sprite.Group()
        self.show_grid, self.selected_type, self.wave_num = True, "basic", 1
        self.spawn_queue, self.spawn_timer, self.in_wave, self.show_info, self.show_sound = [], 0, False, False, False
        self.selected_tower = None
        self.ui_panel_x = WIDTH - 200
        
        self.shop_buttons = {t: pygame.Rect(self.ui_panel_x+20, 150+i*50, 160, 40) for i, t in enumerate(TOWER_TYPES.keys())}
        self.start_wave_rect = pygame.Rect(self.ui_panel_x+20, 360, 160, 45)
        self.speed_btn_rect = pygame.Rect(self.ui_panel_x+20, 415, 160, 40)
        self.grid_toggle_rect = pygame.Rect(self.ui_panel_x+20, HEIGHT-140, 160, 40)
        self.sound_btn_rect = pygame.Rect(self.ui_panel_x+20, HEIGHT-95, 160, 40)
        self.info_btn_rect = pygame.Rect(self.ui_panel_x+20, HEIGHT-50, 160, 40)
        
        self.info_rect = pygame.Rect(250, 80, 750, 550)
        self.sound_ctrls = {
            "music": {"up": pygame.Rect(750, 200, 40, 40), "down": pygame.Rect(650, 200, 40, 40)},
            "shoot": {"up": pygame.Rect(750, 260, 40, 40), "down": pygame.Rect(650, 260, 40, 40)},
            "hit":   {"up": pygame.Rect(750, 320, 40, 40), "down": pygame.Rect(650, 320, 40, 40)},
            "base":  {"up": pygame.Rect(750, 380, 40, 40), "down": pygame.Rect(650, 380, 40, 40)}
        }
        
        self.restart_btn_rect = pygame.Rect(WIDTH//2 - 100, 450, 200, 60)

    def prepare_wave(self):
        if self.won or self.lost: return
        self.spawn_queue = []
        w = self.wave_num
        for _ in range(10 + (w - 1) * 5): self.spawn_queue.append("soldier")
        if w >= 5: 
            for _ in range(2 + (w - 5) * 2): self.spawn_queue.append("vehicle")
        if w >= 10: 
            for _ in range(1 + (w - 10) * 2): self.spawn_queue.append("tank")
        if w % 15 == 0:
            hp_mult = 1.8 ** (w // 15 - 1)
            self.spawn_queue.append(("boss", ENEMY_TYPES["boss"]["hp"] * hp_mult))
        self.in_wave = True

    def handle_click(self, mouse_pos):
        if self.won or self.lost:
            if self.restart_btn_rect.collidepoint(mouse_pos):
                self.need_restart = True
            return

        if self.show_info or self.show_sound:
            close_r = pygame.Rect(self.info_rect.right-40, self.info_rect.y+10, 30, 30)
            if close_r.collidepoint(mouse_pos): self.show_info = self.show_sound = False
            if self.show_sound:
                for s_type, btns in self.sound_ctrls.items():
                    if btns["up"].collidepoint(mouse_pos): self.sound.change_vol(s_type, 0.1)
                    if btns["down"].collidepoint(mouse_pos): self.sound.change_vol(s_type, -0.1)
            return

        if self.info_btn_rect.collidepoint(mouse_pos): self.show_info = True; return
        if self.sound_btn_rect.collidepoint(mouse_pos): self.show_sound = True; return
        if self.grid_toggle_rect.collidepoint(mouse_pos): self.show_grid = not self.show_grid; return
        if self.start_wave_rect.collidepoint(mouse_pos) and not self.in_wave: self.prepare_wave(); return
        if self.speed_btn_rect.collidepoint(mouse_pos): self.game_speed = 2 if self.game_speed == 1 else 1; return
        
        for t_name, rect in self.shop_buttons.items():
            if rect.collidepoint(mouse_pos): self.selected_type = t_name; self.selected_tower = None; return
        
        gx, gy = mouse_pos[0]//TILE_SIZE, mouse_pos[1]//TILE_SIZE
        if mouse_pos[0] < self.ui_panel_x:
            clicked_t = next((t for t in self.towers if t.gx == gx and t.gy == gy), None)
            if clicked_t: self.selected_tower = clicked_t
            else:
                if self.selected_tower:
                    t = self.selected_tower
                    sel_r = pygame.Rect(t.rect.centerx - 20, t.rect.y - 40, 40, 35)
                    if sel_r.collidepoint(mouse_pos):
                        # Predaj s limitom 500$
                        self.money = min(500, self.money + TOWER_TYPES[t.type]["cost"])
                        t.kill(); self.selected_tower = None
                    else: self.selected_tower = None
                elif self.can_place_tower(gx, gy):
                    self.towers.add(Tower(gx, gy, self.selected_type, self))
                    self.money -= TOWER_TYPES[self.selected_type]["cost"]

    def can_place_tower(self, gx, gy):
        if 0 <= gx < GRID_WIDTH and 0 <= gy < GRID_HEIGHT:
            if self.grid_data[gy][gx] == 0 and self.money >= TOWER_TYPES[self.selected_type]["cost"]:
                return not any(t.gx == gx and t.gy == gy for t in self.towers)
        return False

    def update(self):
        if self.won or self.lost: return
        for _ in range(self.game_speed):
            if self.in_wave:
                self.spawn_timer += 1
                if self.spawn_timer > 40 and self.spawn_queue:
                    data = self.spawn_queue.pop(0)
                    if isinstance(data, tuple):
                        e = Enemy(self.waypoints, data[0], self)
                        e.hp = e.max_hp = data[1]; self.enemies.add(e)
                    else: self.enemies.add(Enemy(self.waypoints, data, self))
                    self.spawn_timer = 0
                if not self.spawn_queue and not self.enemies: 
                    if self.wave_num == 15: self.won = True; self.in_wave = False
                    else: self.in_wave, self.wave_num = False, self.wave_num + 1
            self.enemies.update(); self.projectiles.update()
            for t in self.towers: t.update(self.enemies, self.projectiles)
            for e in self.enemies.copy():
                if e.hp <= 0:
                    # Reward s limitom 500$
                    self.money = min(500, self.money + e.reward)
                    e.kill()
            if self.base_hp <= 0: self.lost = True

    def draw(self, mouse_pos):
        gx, gy = mouse_pos[0]//TILE_SIZE, mouse_pos[1]//TILE_SIZE
        for r in range(GRID_HEIGHT):
            for c in range(GRID_WIDTH):
                rect = pygame.Rect(c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if self.show_grid:
                    color = (30,30,30) if self.grid_data[r][c] == 1 else (15,15,15)
                    if not self.show_info and not self.show_sound and not self.won and not self.lost:
                        if (c, r) == (gx, gy) and mouse_pos[0] < self.ui_panel_x: color = WHITE if self.can_place_tower(c, r) else RED
                    pygame.draw.rect(self.screen, color, rect); pygame.draw.rect(self.screen, (40,40,40), rect, 1)
                elif self.grid_data[r][c] == 1: pygame.draw.rect(self.screen, (25,25,25), rect)
        
        pygame.draw.rect(self.screen, GREEN, (self.path_coords[-1][0]*TILE_SIZE, self.path_coords[-1][1]*TILE_SIZE, TILE_SIZE, TILE_SIZE))
        self.towers.draw(self.screen); self.enemies.draw(self.screen)
        for e in self.enemies: e.draw_hp_bar(self.screen)
        self.projectiles.draw(self.screen)
        if self.selected_tower and self.selected_tower.alive():
            t = self.selected_tower
            pygame.draw.rect(self.screen, WHITE, t.rect, 2)
            sel_r = pygame.Rect(t.rect.centerx - 20, t.rect.y - 40, 40, 35)
            pygame.draw.rect(self.screen, RED, sel_r); f = pygame.font.SysFont(None, 18)
            self.screen.blit(f.render("SELL", True, WHITE), (sel_r.x + 4, sel_r.y + 10))
        self.draw_ui()
        if self.show_info: self.draw_pop("GAME INFO", ["TOWERS: B-Basic, D-Double, F-Fire, S-Freeze", "MAX GOLD LIMIT: 500$", "ENEMIES (HP +75%):", f"Soldier: 61 HP / 2.5 SPD", f"Vehicle: 368 HP / 3.5 SPD", f"Tank: 1531 HP / 1.2 SPD", f"Boss: 10719 HP (W15)", "BEAT WAVE 15 TO WIN!"])
        if self.show_sound: self.draw_sound_menu()
        if self.won: self.draw_end_screen("VICTORY!", GREEN)
        if self.lost: self.draw_end_screen("GAME OVER", RED)

    def draw_ui(self):
        pygame.draw.rect(self.screen, (20,20,20), (self.ui_panel_x, 0, 200, HEIGHT))
        f = pygame.font.SysFont(None, 26)
        self.screen.blit(f.render(f"Gold: {self.money}$", True, GOLD), (self.ui_panel_x+20, 20))
        self.screen.blit(f.render(f"HP: {self.base_hp}", True, RED), (self.ui_panel_x+20, 45))
        self.screen.blit(f.render(f"Wave: {self.wave_num}/15", True, WHITE), (self.ui_panel_x+20, 70))
        rem = len(self.spawn_queue) + len(self.enemies)
        self.screen.blit(f.render(f"Enemies: {rem}", True, CYAN), (self.ui_panel_x+20, 95))
        fs = pygame.font.SysFont(None, 20)
        for t_name, rect in self.shop_buttons.items():
            pygame.draw.rect(self.screen, TOWER_TYPES[t_name]["color"], rect)
            if self.selected_type == t_name: pygame.draw.rect(self.screen, WHITE, rect.inflate(4,4), 2)
            self.screen.blit(fs.render(f"{t_name.upper()} {TOWER_TYPES[t_name]['cost']}$", True, BLACK), (rect.x+10, rect.y+10))
        btn_c = GREEN if not self.in_wave else (40,40,40)
        pygame.draw.rect(self.screen, btn_c, self.start_wave_rect)
        self.screen.blit(fs.render("START WAVE" if not self.in_wave else "IN PROGRESS", True, BLACK if not self.in_wave else WHITE), (self.start_wave_rect.x+20, self.start_wave_rect.y+12))
        pygame.draw.rect(self.screen, ORANGE, self.speed_btn_rect)
        self.screen.blit(fs.render(f"SPEED: {self.game_speed}X", True, BLACK), (self.speed_btn_rect.x+40, self.speed_btn_rect.y+10))
        for r, txt, col in [(self.grid_toggle_rect, "GRID", (60,60,60)), (self.sound_btn_rect, "SOUND", (80,40,120)), (self.info_btn_rect, "INFO", BLUE)]:
            pygame.draw.rect(self.screen, col, r); self.screen.blit(fs.render(txt, True, WHITE), (r.x+50, r.y+10))

    def draw_pop(self, title, lines):
        surf = pygame.Surface(self.info_rect.size); surf.set_alpha(245); surf.fill((5,5,5))
        self.screen.blit(surf, self.info_rect.topleft); pygame.draw.rect(self.screen, WHITE, self.info_rect, 2)
        close_r = pygame.Rect(self.info_rect.right-40, self.info_rect.y+10, 30, 30)
        pygame.draw.rect(self.screen, RED, close_r); f = pygame.font.SysFont(None, 28)
        self.screen.blit(f.render("X", True, WHITE), (close_r.x+8, close_r.y+5))
        self.screen.blit(f.render(title, True, GOLD), (self.info_rect.x+30, self.info_rect.y+30))
        for i, l in enumerate(lines): self.screen.blit(f.render(l, True, WHITE), (self.info_rect.x+30, self.info_rect.y+80+i*28))

    def draw_sound_menu(self):
        self.draw_pop("SOUND SETTINGS", ["Adjust individual volumes:"])
        f_small, f_btn = pygame.font.SysFont(None, 24), pygame.font.SysFont(None, 32)
        y_off = 200
        for s_type, btns in self.sound_ctrls.items():
            vol = getattr(self.sound, f"vol_{s_type}")
            txt = f"{s_type.upper()} VOLUME: {int(vol*100)}%"
            self.screen.blit(f_small.render(txt, True, WHITE), (self.info_rect.x+50, y_off + 10))
            pygame.draw.rect(self.screen, RED, btns["down"]); self.screen.blit(f_btn.render("-", True, WHITE), (btns["down"].x+15, btns["down"].y+5))
            pygame.draw.rect(self.screen, GREEN, btns["up"]); self.screen.blit(f_btn.render("+", True, BLACK), (btns["up"].x+12, btns["up"].y+5))
            y_off += 60

    def draw_end_screen(self, title, color):
        s = pygame.Surface((WIDTH, HEIGHT)); s.set_alpha(200); s.fill(BLACK)
        self.screen.blit(s, (0,0))
        f_big = pygame.font.SysFont(None, 120)
        f_btn = pygame.font.SysFont(None, 50)
        self.screen.blit(f_big.render(title, True, color), (WIDTH//2 - 250, 250))
        pygame.draw.rect(self.screen, (50, 50, 50), self.restart_btn_rect)
        pygame.draw.rect(self.screen, WHITE, self.restart_btn_rect, 2)
        self.screen.blit(f_btn.render("RESTART", True, WHITE), (self.restart_btn_rect.x + 25, self.restart_btn_rect.y + 12))