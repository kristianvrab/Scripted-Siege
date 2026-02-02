import pygame
from engine import game_window, game
from game.config import WIDTH, HEIGHT, FPS

pygame.init()

# ---------- WINDOW ----------
window = game_window.GameWindow(WIDTH, HEIGHT, "Scripted Siege")

# ---------- GAME & SOUND ----------
siege = game.Game(window.screen)
sound = siege.sound 

clock = pygame.time.Clock()

# ---------- MAIN LOOP ----------
while window.running:
    # Spracovanie vstupu
    window.running = siege.processInput()

    # Update
    siege.update()

    # Render
    window.screen.fill((0, 0, 0))
    siege.render()
    pygame.display.update()

    clock.tick(FPS)

pygame.quit()
