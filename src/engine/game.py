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
        self.level = Level(screen, self.sound)
        self.should_quit = False

        self._mbuttons_used = [pygame.BUTTON_LEFT]
        self._keys_used = [pygame.K_ESCAPE]
        self._mbuttons_pressed = []
        self._keys_pressed = []

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
        if self.should_quit: return False

        if self.state == "menu":
            if self.mousePressed(pygame.BUTTON_LEFT):
                if self.menu.buttons["play"].collidepoint(mouse_pos):
                    self.level = Level(self.screen, self.sound)
                    self.state = "in_game"
                if self.menu.buttons["quit"].collidepoint(mouse_pos):
                    return False

        elif self.state == "in_game":
            if self.keyPressed(pygame.K_ESCAPE):
                self.state = "menu"
            if self.mousePressed(pygame.BUTTON_LEFT):
                self.level.handle_click(mouse_pos)

        return True

    def update(self):
        if self.state == "in_game":
            self.level.update()
            # Reset hry ak hrac klikol na RESTART
            if self.level.need_restart:
                self.level = Level(self.screen, self.sound)

    def render(self, mouse_pos):
        if self.state == "menu":
            self.menu.draw(mouse_pos)
        elif self.state == "in_game":
            self.level.draw(mouse_pos)

    def mousePressed(self, button):
        return button in self._mbuttons_pressed

    def keyPressed(self, key):
        return key in self._keys_pressed