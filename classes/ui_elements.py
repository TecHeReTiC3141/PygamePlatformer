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


class ChangeStateButton(Button):
    state = ""


class LevelChangeStateButton(ChangeStateButton):
    pass


class GameChangeStateButton(ChangeStateButton):
    pass


class DirectionButton(LevelChangeStateButton):
    image = pygame.image.load(ui_images / 'Direction_button.png')
    dirs = {'d': 0, 'l': 90, 'u': 180, 'r': 270}
    state = 'game'

    def __init__(self, x, y, size: tuple, dir):
        self.image = pygame.transform.scale(pygame.transform.rotate(self.image,
                                                                    self.dirs[dir]), size)
        self.rect = self.image.get_rect(topleft=(x, y))


class PauseButton(LevelChangeStateButton):
    image = pygame.image.load(ui_images / 'Pause_button.png')
    state = 'pause'


class UnpauseButton(LevelChangeStateButton):
    image = pygame.image.load(ui_images / 'Pause_button.png')
    state = 'game'

    def __init__(self, x, y, size: tuple, state):
        super().__init__(x, y, size)
        self.state = state


class UI_container(UI):  # menus, etc

    def __init__(self, x, y, size: tuple, content: list[UI]):
        self.active = False
        super().__init__(x, y, size)
        self.content = content

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

    def update(self, mouse: tuple):
        pass
