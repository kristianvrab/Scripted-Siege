import pygame
from engine import game_window, game
from engine.sound_manager import SoundManager
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
    mouse_pos = pygame.mouse.get_pos()

    # Spracovanie vstupu
    window.running = siege.processInput(mouse_pos)

    # ---------- GAME STATE MUSIC ----------
    if siege.state == "menu":
        sound.play_menu()
    elif siege.state == "in_game":
        sound.play_game()

    # Update
    siege.update()

    # Render
    window.screen.fill((0, 0, 0))
    siege.render(mouse_pos)
    pygame.display.update()

    clock.tick(FPS)

pygame.quit()
