import pygame
from scripts.const import *

class GameManager:

    def __init__(self, display: pygame.Surface, res=(DISP_WIDTH, DISP_HEIGHT)):
        self.game_state = 'main_menu'
        self.display = display
        self.is_paused = False
        self.difficulty = 'Medium'
        self.res = res
        self.surf = pygame.Surface(res)
        self.clock = pygame.time.Clock()

        # settings
        self.show_debug = True

    def change_state(self, new_state):
        pass


    def update(self, res: tuple, fullscreen: bool, debug: bool):
        if fullscreen:
            self.display = pygame.display.set_mode(res, pygame.FULLSCREEN)
        else:
            self.display = pygame.display.set_mode(res)
        self.res = res
        self.show_debug = debug
