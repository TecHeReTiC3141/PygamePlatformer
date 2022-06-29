import pygame
from random import *
from math import *

pygame.init()

DISP_WIDTH, DISP_HEIGHT = 1080, 720
ASPECT_RATIO = DISP_WIDTH / DISP_HEIGHT
FPS = 60

BLOCK_SIZE = 64
TILED_SIZE = 128
SCALE = BLOCK_SIZE / TILED_SIZE

directions = ['up', 'down', 'left', 'right']

mock_display = pygame.display.set_mode((40, 40))

info_font = pygame.font.Font(None, 40)