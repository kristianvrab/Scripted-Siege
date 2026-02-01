import pygame
from game.menu import Menu
from game.level import Level
from engine.sound_manager import SoundManager

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.sound = SoundManager()
        self.state = "menu"
        self.menu = Menu(screen)
        self.level = Level(screen, self.sound)  # Level dostane sound
        self.should_quit = False

        # input tracking
        self._mbuttons_used = [pygame.BUTTON_LEFT]
        self._keys_used = [pygame.K_ESCAPE]
        self._mbuttons_pressed = []
        self._keys_pressed = []

    # ---------- INPUT ----------
    def collectInput(self):
        self._mbuttons_pressed.clear()
        self._keys_pressed.clear()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.should_quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in self._mbuttons_used:
                    self._mbuttons_pressed.append(event.button)
            elif event.type == pygame.KEYDOWN:
                if event.key in self._keys_used:
                    self._keys_pressed.append(event.key)

    def processInput(self, mouse_pos):
        self.collectInput()
        if self.should_quit:
            return False

        # --- MENU ---
        if self.state == "menu":
            if self.mousePressed(pygame.BUTTON_LEFT):
                if self.menu.buttons["play"].collidepoint(mouse_pos):
                    self.level = Level(self.screen, self.sound)  # prepni na novú hru
                    self.state = "in_game"
                if self.menu.buttons["quit"].collidepoint(mouse_pos):
                    return False

        # --- IN GAME ---
        elif self.state == "in_game":
            if self.keyPressed(pygame.K_ESCAPE):
                self.state = "menu"
            if self.mousePressed(pygame.BUTTON_LEFT):
                self.level.handle_click(mouse_pos)

        # --- GAME OVER ---
        elif self.state == "game_over":
            if self.keyPressed(pygame.K_ESCAPE):
                self.state = "menu"

        return True

    # ---------- UPDATE ----------
    def update(self):
        if self.state == "in_game":
            self.level.update()
            if self.level.base_hp <= 0:
                self.state = "game_over"

    # ---------- RENDER ----------
    def render(self, mouse_pos):
        if self.state == "menu":
            self.menu.draw(mouse_pos)
        elif self.state == "in_game":
            self.level.draw(mouse_pos)
        elif self.state == "game_over":
            self.screen.fill((50, 0, 0))
            font = pygame.font.SysFont(None, 100)
            self.screen.blit(font.render("GAME OVER", True, (255, 255, 255)), (400, 300))

    # ---------- INPUT HELPERS ----------
    def mousePressed(self, button):
        return button in self._mbuttons_pressed

    def keyPressed(self, key):
        return key in self._keys_pressed
