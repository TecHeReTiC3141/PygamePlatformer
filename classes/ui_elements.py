from pathlib import Path
from classes.gui_elements import *

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


class LevelQuitButton(Button):
    next_level = True


class GUI_trigger(Button):

    def __init__(self, x, y, size: tuple, gui_class: type):
        super().__init__(x, y, size)
        self.gui = gui_class


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


class QuitButton(GUI_trigger):
    image = pygame.image.load(ui_images / 'Exit_button.png')


class SettingsButton(GUI_trigger):
    image = pygame.image.load(ui_images / 'Settings_button.png')


class RetryButton(LevelQuitButton):
    next_level = False
    image = pygame.image.load(ui_images / 'Retry_button.png')


class NextLevelButton(LevelQuitButton):
    image = pygame.image.load(ui_images / 'Pause_button.png')


class UI_container(UI):  # menus, etc

    def __init__(self, x, y, size: tuple, content: list[UI], end_point: tuple):
        self.active = False
        super().__init__(x, y, size)
        self.content = content
        for ui in self.content:
            self.image.blit(ui.image, ui.rect.topleft)
            ui.rect.x += self.rect.x
            ui.rect.y += self.rect.y
            print(ui.rect)
        self.init_pos = self.rect.center
        self.end_pos = end_point

    def move(self, speed=20):
        move = pygame.math.Vector2(0, 0)
        if self.active and self.rect.center != self.end_pos:
            move.x = -speed if self.rect.centerx > self.end_pos[0] else speed \
                if self.rect.centerx < self.end_pos[0] else 0

            move.y = -speed if self.rect.centery > self.end_pos[1] else speed \
                if self.rect.centery < self.end_pos[1] else 0

        elif not self.active and self.rect.center != self.init_pos:
            move.x = -speed if self.rect.centerx > self.init_pos[0] else speed \
                if self.rect.centerx < self.init_pos[0] else 0

            move.y = -speed if self.rect.centery > self.init_pos[1] else speed \
                if self.rect.centery < self.init_pos[1] else 0

        if move.length():
            self.rect.move_ip(move)
            for ui in self.content:
                ui.rect.move_ip(move)

    def draw(self, surface: pygame.Surface, speed=20):
        self.move(speed)
        surface.blit(self.image, self.rect)

    def update(self, mouse: tuple):
        pass


class PauseMenu(UI_container):
    image = pygame.image.load(ui_images / 'Pause_menu.png')

    def __init__(self, x, y, size: tuple, content: list[UI], end_point: tuple,
                 level_name: str, cur_time):
        super().__init__(x, y, size, content, end_point)
        self.image.blit(menu_font.render(level_name, True, '#9C6409'), (80, 115))
        self.image.blit(menu_font.render('Pause', True, '#9C6409'), (250, 10))
        self.init_pos = self.rect.center
        self.end_pos = end_point
        self.time = cur_time

    def draw(self, surface: pygame.Surface, speed=20):
        pygame.draw.rect(self.image, '#B8B1A6', (240, 120, 200, 40))
        self.image.blit(menu_font.render(strftime('%M:%S', gmtime(self.time)), True, '#9C6409'),
                        (240, 110))
        super().draw(surface, speed)


class EndLevelMenu(UI_container):
    image = pygame.image.load(ui_images / 'Pause_menu.png')

    def __init__(self, x, y, size: tuple, content: list[UI], end_point: tuple,
                 level_name: str, cur_time, max_score, player_score):
        super().__init__(x, y, size, content, end_point)
        self.image.blit(menu_font.render(level_name + " passed!", True, '#9C6409'), (160, 45))
        self.image.blit(menu_font.render('Time', True, '#9C6409'), (330, 120))
        self.image.blit(menu_font.render(strftime('%M:%S', gmtime(cur_time)), True, '#9C6409'), (480, 120))
        self.init_pos = self.rect.center
        self.end_pos = end_point

        self.cur_score = 0
        self.player_score = player_score
        self.max_score = max_score

    def draw(self, surface: pygame.Surface, speed=20):
        if self.cur_score < self.player_score:
            self.cur_score += 1

        pygame.draw.rect(self.image, '#eecc67', (240, 120, 200, 40))
        self.image.blit(menu_font.render(f'{self.cur_score} / {self.max_score}', True, '#9C6409'), (85, 120))

        super().draw(surface, speed)
