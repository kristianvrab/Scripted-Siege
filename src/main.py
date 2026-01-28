import pygame
from engine import game_window, game
from game.config import WIDTH, HEIGHT, FPS

pygame.init()

window = game_window.GameWindow(WIDTH, HEIGHT, "Scripted Siege")
siege = game.Game(window.screen)

clock = pygame.time.Clock()

# mainloop
while window.running:
    mouse_pos = pygame.mouse.get_pos()

    window.running = siege.processInput(mouse_pos)

    siege.update()

    window.screen.fill("black")
    siege.render(mouse_pos)
    pygame.display.update()

    clock.tick(FPS)

pygame.quit()
