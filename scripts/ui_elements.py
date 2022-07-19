import pygame
from pathlib import Path

ui_images = Path('resources/images/ui')

class UI:

    image = pygame.Surface((50, 50))

    def __init__(self, x, y, size: tuple):
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

    def update(self, mouse: tuple):
        pass


class Button(UI):
    pass

class LevelChangeStateButton(Button):
    state = ""

class GameChangeStateButton(Button):
    state = ""

class DirectionButton(LevelChangeStateButton):
    image = pygame.image.load(ui_images / 'Direction_button.png')
    dirs = {'d': 0, 'l': 90, 'u': 180, 'r': 270}
    state = 'main_game'

    def __init__(self, x, y, size: tuple, dir):
        self.image = pygame.transform.scale(pygame.transform.rotate(self.image, self.dirs[dir]), size)
        self.rect = self.image.get_rect(topleft=(x, y))


class PauseButton(LevelChangeStateButton):
    image = pygame.image.load(ui_images / 'Pause_button.png')
    state = 'pause_menu'




