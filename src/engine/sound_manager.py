import pygame
class SoundManager:
    def __init__(self):
        pygame.mixer.init()

        self.menu_music = "assets/audio/menu_music.wav"
        self.game_music = "assets/audio/game_music.wav"
        self.shoot = pygame.mixer.Sound("assets/audio/tower_shoot.mp3")
        self.hit = pygame.mixer.Sound("assets/audio/enemy_hit.wav")
        self.base_hit = pygame.mixer.Sound("assets/audio/base_hit.mp3")

        self.current = None

    def play_menu(self):
        if self.current != "menu":
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.menu_music)
            pygame.mixer.music.play(-1)
            self.current = "menu"

    def play_game(self):
        if self.current != "game":
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.game_music)
            pygame.mixer.music.play(-1)
            self.current = "game"

    def stop(self):
        pygame.mixer.music.stop()
        self.current = None
