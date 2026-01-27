import pygame
from engine import game_window, game

# ---------- INITIALIZATION ----------
pygame.init()
WIDTH, HEIGHT = 1280, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scripted Siege")
CLOCK = pygame.time.Clock()

# ---------- ENGINE SETUP ----------
ENGINE_WINDOW = game_window.GameWindow(WIDTH, HEIGHT, "Scripted Siege")
SIEGE = game.Game()

# ---------- GLOBAL FONTS ----------
FONT_TITLE = pygame.font.SysFont(None, 100)
FONT_MENU = pygame.font.SysFont(None, 50)

# ---------- CLASSES ----------
class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = {}
    
    def draw(self):
        mouse_pos = pygame.mouse.get_pos()

        # Title
        title_text = FONT_TITLE.render("SCRIPTED SIEGE", True, "white")
        title_rect = title_text.get_rect(center=(WIDTH//2, 120))
        self.screen.fill("gray10")
        self.screen.blit(title_text, title_rect)

        # Play button
        play_text = FONT_MENU.render("Play", True, "white")
        play_rect = play_text.get_rect(center=(WIDTH//2, 300))
        if play_rect.collidepoint(mouse_pos):
            play_text = FONT_MENU.render("Play", True, "red")
        self.screen.blit(play_text, play_rect)
        self.buttons["play"] = play_rect

        # Quit button
        quit_text = FONT_MENU.render("Quit", True, "white")
        quit_rect = quit_text.get_rect(center=(WIDTH//2, 380))
        if quit_rect.collidepoint(mouse_pos):
            quit_text = FONT_MENU.render("Quit", True, "red")
        self.screen.blit(quit_text, quit_rect)
        self.buttons["quit"] = quit_rect

class GameEngine:
    def __init__(self, siege, window):
        self.siege = siege
        self.window = window

    def run(self):
        # Run ONE frame of the engine
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.window.running = False

        self.siege.processInput()
        self.siege.update()
        self.siege.render()

# ---------- MAIN LOOP ----------
def main():
    menu_screen = Menu(SCREEN)
    engine = GameEngine(SIEGE, ENGINE_WINDOW)

    game_state = "menu"
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()
        SCREEN.fill("black")  # default background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if game_state == "game" and event.key == pygame.K_ESCAPE:
                    game_state = "menu"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_state == "menu":
                    if menu_screen.buttons["play"].collidepoint(mouse_pos):
                        game_state = "game"
                    elif menu_screen.buttons["quit"].collidepoint(mouse_pos):
                        running = False

        # DRAW STATES
        if game_state == "menu":
            menu_screen.draw()
        elif game_state == "game":
            engine.run()

        pygame.display.update()
        CLOCK.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()