import pygame

class GameWindow:
    def __init__(self, width, height, title):
        self.running = True

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
