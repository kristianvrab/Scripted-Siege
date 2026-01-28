import pygame
from config import WIDTH,HEIGHT
class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont(None, 80)
        self.font_button = pygame.font.SysFont(None, 40)
        self.buttons = {}

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()

        self.screen.fill("gray10")

        # Title
        title = self.font_title.render("SCRIPTED SIEGE", True, "white")
        title_rect = title.get_rect(center=(WIDTH//2, 120))
        self.screen.blit(title, title_rect)

        # Play button
        play_text = self.font_button.render("Play", True, "white")
        play_rect = play_text.get_rect(center=(WIDTH//2, 280))
        if play_rect.collidepoint(mouse_pos):
            play_text = self.font_button.render("Play", True, "red")

        self.screen.blit(play_text, play_rect)
        self.buttons["play"] = play_rect

        # Quit button
        quit_text = self.font_button.render("Quit", True, "white")
        quit_rect = quit_text.get_rect(center=(WIDTH//2, 340))
        if quit_rect.collidepoint(mouse_pos):
            quit_text = self.font_button.render("Quit", True, "red")

        self.screen.blit(quit_text, quit_rect)
        self.buttons["quit"] = quit_rect