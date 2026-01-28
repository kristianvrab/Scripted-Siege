import pygame
from engine import game_window, game
from config import WIDTH,HEIGHT

pygame.init()

window = game_window.GameWindow(WIDTH, HEIGHT, "Scripted Siege")
siege = game.Game(window.screen)

clock = pygame.time.Clock()

# mainloop
while window.running:
    mouse_pos = pygame.mouse.get_pos()

    window.running = siege.processInput(mouse_pos)

    siege.update()

    siege.render(mouse_pos)
    pygame.display.update()

    clock.tick(60)

pygame.quit()
