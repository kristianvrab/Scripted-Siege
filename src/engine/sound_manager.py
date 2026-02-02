import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.menu_music = "assets/audio/menu_music.wav"
        self.game_music = "assets/audio/game_music.wav"
        self.shoot = pygame.mixer.Sound("assets/audio/tower_shoot.mp3")
        self.hit = pygame.mixer.Sound("assets/audio/enemy_hit.wav")
        self.base_hit = pygame.mixer.Sound("assets/audio/base_hit.mp3")
        
        # Samostatné hlasitosti
        self.vol_music = 0.5
        self.vol_shoot = 0.5
        self.vol_hit = 0.5
        self.vol_base = 0.5
        
        self.current = None
        self.update_all_volumes()

    def update_all_volumes(self):
        pygame.mixer.music.set_volume(self.vol_music)
        self.shoot.set_volume(self.vol_shoot)
        self.hit.set_volume(self.vol_hit)
        self.base_hit.set_volume(self.vol_base)

    def change_vol(self, type, amt):
        if type == "music": self.vol_music = max(0, min(1, self.vol_music + amt))
        elif type == "shoot": self.vol_shoot = max(0, min(1, self.vol_shoot + amt))
        elif type == "hit": self.vol_hit = max(0, min(1, self.vol_hit + amt))
        elif type == "base": self.vol_base = max(0, min(1, self.vol_base + amt))
        self.update_all_volumes()

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