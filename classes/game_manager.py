import pygame
from scripts.const import *

class GameManager:

    def __init__(self, display: pygame.Surface, res=(DISP_WIDTH, DISP_HEIGHT)):
        self.game_state = 'game'
        self.display = display
        self.is_paused = False
        self.difficulty = 'Medium'
        self.res = res
        self.surf = pygame.Surface(res)

    def change_state(self, new_state):
        pass

    def update(self, res: tuple):
        pass