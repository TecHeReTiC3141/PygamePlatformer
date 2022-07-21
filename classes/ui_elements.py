from pathlib import Path
from scripts.const import *

ui_images = Path('resources/images/ui')


class UI:
    image = pygame.Surface((50, 50))
    active = True

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

class QuitButton(GameChangeStateButton):
    image = pygame.image.load(ui_images / 'Exit_button.png')


class SettingsButton(LevelChangeStateButton):
    image = pygame.image.load(ui_images / 'Settings_button.png')


class UI_container(UI):  # menus, etc

    def __init__(self, x, y, size: tuple, content: list[UI], end_point: tuple, level_name: str):
        self.active = False
        super().__init__(x, y, size)
        self.content = content
        for ui in self.content:
            self.image.blit(ui.image, ui.rect.topleft)
            ui.rect.x += self.rect.x
            ui.rect.y += self.rect.y
        self.image.blit(menu_font.render(level_name, True, '#9C6409'), (80, 115))
        self.image.blit(menu_font.render('Pause', True, '#9C6409'), (250, 15))
        self.init_pos = self.rect.center
        self.end_pos = end_point

    def move(self, speed=20):
        move = pygame.math.Vector2(0, 0)
        if self.active and self.rect.center != self.end_pos:
            move.x = -speed if self.rect.centerx > self.end_pos[0] else speed \
                if self.rect.centerx < self.end_pos[0] else 0

            move.y = -speed if self.rect.centery > self.end_pos[1] else speed \
                if self.rect.centery < self.end_pos[1] else 0
            print(self.rect)
        elif not self.active and self.rect.center != self.init_pos:
            move.x = -speed if self.rect.centerx > self.init_pos[0] else speed\
                if self.rect.centerx < self.init_pos[0] else 0

            move.y = -speed if self.rect.centery > self.init_pos[1] else speed \
                if self.rect.centery < self.init_pos[1] else 0
        else:
            for ui in self.content:
                ui.rect.x += self.end_pos[0] - self.init_pos[0]
                ui.rect.y += self.end_pos[1] - self.init_pos[1]
        self.rect.move_ip(move)

    def draw(self, surface: pygame.Surface, speed=5):
        self.move(speed)
        surface.blit(self.image, self.rect)

    def update(self, mouse: tuple):
        pass


class PauseMenu(UI_container):
    image = pygame.image.load(ui_images / 'Pause_menu.png')
    pass
