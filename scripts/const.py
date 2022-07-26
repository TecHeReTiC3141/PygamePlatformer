import pygame
from random import *
from math import *
from time import *

pygame.init()

DISP_WIDTH, DISP_HEIGHT = 1280, 720
ASPECT_RATIO = DISP_WIDTH / DISP_HEIGHT
FPS = 60

BLOCK_SIZE = 64
TILED_SIZE = 128
SCALE = BLOCK_SIZE / TILED_SIZE

directions = ['up', 'down', 'left', 'right']

mock_display = pygame.display.set_mode((40, 40))

info_font = pygame.font.Font(None, 40)
stats_font = pygame.font.SysFont('Cambria', 50)
menu_font = pygame.font.SysFont('Ubuntu', 50)

# heart = pygame.image.load('resources/images/interface/heart.png').convert_alpha()

blur = pygame.Surface((DISP_WIDTH, DISP_HEIGHT))
blur.set_alpha(100)
