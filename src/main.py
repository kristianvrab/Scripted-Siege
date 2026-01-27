import pygame
from engine import game_window, game

pygame.init()

WIDTH, HEIGHT = 800, 600

window = game_window.GameWindow(WIDTH, HEIGHT, "Scripted Siege")
siege = game.Game()

# mainloop
while window.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            window.running = False

    siege.processInput()

    siege.update()

    siege.render()

pygame.quit()
