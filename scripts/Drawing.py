import pygame
from scripts.const import *

class Drawing:

    def __init__(self, surf: pygame.Surface):
        self.surf = surf

        self.background_surf = pygame.Surface(self.surf.get_size())
        self.background_surf.fill('grey')

    def background(self):
        self.surf.blit(self.background_surf, (0, 0))