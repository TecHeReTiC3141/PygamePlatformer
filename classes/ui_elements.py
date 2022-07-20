from pathlib import Path
from scripts.const import *

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

    def __init__(self, x, y, size: tuple, content: list[UI], align='center'):
        self.active = False
        super().__init__(x, y, size)
        self.content = content
        for ui in self.content:
            self.image.blit(ui.image, ui.rect.topleft)
            ui.rect.x += self.rect.x
            ui.rect.y += self.rect.y

        self.align = align
        self.init_pos = self.rect.center

    def draw(self, surface: pygame.Surface, speed=5):
        move = pygame.math.Vector2(0, 0)
        if self.active:
            if self.align == 'center' and self.rect.center != (DISP_WIDTH // 2, DISP_HEIGHT // 2):
                move.x = -speed if self.rect.centerx > DISP_WIDTH // 2 else speed
                move.y = -speed if self.rect.centery > DISP_HEIGHT // 2 else speed
        else:
            if self.rect.center != self.init_pos:
                move.x = -speed if self.rect.centerx > self.init_pos[0] else speed
                move.y = -speed if self.rect.centery > self.init_pos[0] else speed
        self.rect.move_ip(move)
        surface.blit(self.image, self.rect)

    def update(self, mouse: tuple):
        pass


class MainMenu(UI_container):

    pass
