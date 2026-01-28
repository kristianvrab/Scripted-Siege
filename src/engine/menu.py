import pygame
from config import WIDTH

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont(None, 80)
        self.font_button = pygame.font.SysFont(None, 40)
        self.buttons = {}

        # Pre-render text
        self.title_text = self.font_title.render("SCRIPTED SIEGE", True, "white")
        self.play_text = self.font_button.render("Play", True, "white")
        self.play_text_hover = self.font_button.render("Play", True, "red")
        self.quit_text = self.font_button.render("Quit", True, "white")
        self.quit_text_hover = self.font_button.render("Quit", True, "red")

        # Precompute rects once (positions are static)
        self.title_rect = self.title_text.get_rect(center=(WIDTH//2, 120))
        self.play_rect = self.play_text.get_rect(center=(WIDTH//2, 280))
        self.quit_rect = self.quit_text.get_rect(center=(WIDTH//2, 340))

        # Store rects for external access
        self.buttons["play"] = self.play_rect
        self.buttons["quit"] = self.quit_rect

    def draw(self, mouse_pos):
        self.screen.fill("gray10")

        # Title
        self.screen.blit(self.title_text, self.title_rect)

        # Mozno by som presunul cast do inputu
        # Play button
        if self.play_rect.collidepoint(mouse_pos):
            self.screen.blit(self.play_text_hover, self.play_rect)
        else:
            self.screen.blit(self.play_text, self.play_rect)

        # Quit button
        if self.quit_rect.collidepoint(mouse_pos):
            self.screen.blit(self.quit_text_hover, self.quit_rect)
        else:
            self.screen.blit(self.quit_text, self.quit_rect)
