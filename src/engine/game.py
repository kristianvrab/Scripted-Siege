import pygame
from engine.menu import Menu

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

    def processInput(self):
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if self.state == "menu":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.menu.buttons.get("play") and self.menu.buttons["play"].collidepoint(mouse_pos):
                        self.state = "in_game"

                    if self.menu.buttons.get("quit") and self.menu.buttons["quit"].collidepoint(mouse_pos):
                        return False

            elif self.state == "in_game":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.state = "menu"

        return True

    def update(self):
        if self.state == "in_game":
            pass  

    def render(self):
        if self.state == "menu":
            self.menu.draw()

        elif self.state == "in_game":
            self.screen.fill("black")
            