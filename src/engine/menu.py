import pygame
from config import WIDTH,HEIGHT

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont(None, 120)
        self.font_button = pygame.font.SysFont(None, 80)
        self.buttons = {}
        # load image for background
        self.background = pygame.image.load("./assets/images/menu.png").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))


        # Pre-render text
        self.title_text = self.font_title.render("SCRIPTED SIEGE", True, "black")
        self.play_text = self.font_button.render("Play", True, "grey")
        self.play_text_hover = self.font_button.render("Play", True, "red")
        self.quit_text = self.font_button.render("Quit", True, "grey")
        self.quit_text_hover = self.font_button.render("Quit", True, "red")

        # Precompute rects once (positions are static)
        self.title_rect = self.title_text.get_rect(center=(WIDTH//2, 60))
        self.play_rect = self.play_text.get_rect(center=(WIDTH//2, 270))
        self.quit_rect = self.quit_text.get_rect(center=(WIDTH//2, 360))

        # Store rects for external access
        self.buttons["play"] = self.play_rect
        self.buttons["quit"] = self.quit_rect

    def draw(self, mouse_pos):
        self.screen.fill("gray10")
        self.screen.blit(self.background, (0, 0))

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
