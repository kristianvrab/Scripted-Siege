import pygame
from game.menu import Menu

game_states = [
    "menu",
    "in_game",
    "game_over"
]

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.state = "menu"

        self.menu = Menu(screen)

        self.should_quit = False

        # NOTE: Tu pridaj tlacitdla a klavesy ked ich chces pouzivat
        # Which buttons are used by the game
        self._mbuttons_used = [pygame.BUTTON_LEFT]
        self._keys_used = [pygame.K_ESCAPE]

        # Lists to track per-frame input
        self._mbuttons_pressed = []
        self._keys_pressed = []

    # Automatically collects all input events according to _mbuttons_used and _keys_used
    def collectInput(self):
        self._mbuttons_pressed.clear()
        self._keys_pressed.clear()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.should_quit = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in self._mbuttons_used:
                    self._mbuttons_pressed.append(event.button)

            if event.type == pygame.KEYDOWN:
                if event.key in self._keys_used:
                    self._keys_pressed.append(event.key)

    def processInput(self, mouse_pos):
        self.collectInput()

        if self.should_quit:
            return False

        if self.state == "menu":
            if self.mousePressed(pygame.BUTTON_LEFT):
                if self.menu.buttons["play"].collidepoint(mouse_pos):
                    self.state = "in_game"

                if self.menu.buttons["quit"].collidepoint(mouse_pos):
                    return False

        elif self.state == "in_game":
            if self.keyPressed(pygame.K_ESCAPE):
                self.state = "menu"

        return True

    def update(self):
        if self.state == "in_game":
            pass  

    def render(self, mouse_pos):
        if self.state == "menu":
            self.menu.draw(mouse_pos)

        elif self.state == "in_game":
            pass

    # NOTE: Pouzite tieto funkcie na input handling
    def mousePressed(self, button):
        return button in self._mbuttons_pressed
    
    def keyPressed(self, key):
        return key in self._keys_pressed
