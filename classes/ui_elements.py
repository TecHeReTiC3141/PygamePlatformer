from classes.gui_elements import *
from classes.player import *

ui_images = Path('resources/images/ui')


class UI:
    image = pygame.Surface((50, 50))
    active = True
    requires_offset = False
    requires_player = False

    def __init__(self, x, y, size: tuple):
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.init_pos = self.rect.center
        self.end_pos = self.rect.center

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)

    def update(self, mouse: tuple):
        pass

    def move(self, speed=20) -> pygame.math.Vector2:
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
        return move


class Movable_UI(UI):

    def __init__(self, x, y, size: tuple, end_pos: tuple, delay=0):
        super().__init__(x, y, size)
        self.end_pos = end_pos
        self.delay = delay

    def draw(self, surface: pygame.Surface):
        super().draw(surface)
        self.delay -= 1
        if self.delay <= 0:
            self.move()


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
    gui: type = None


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


class ToLevelMap(GameChangeStateButton):
    image = pygame.Surface((50, 50))
    state = 'game'


class PlayButton(GameChangeStateButton):
    image = pygame.image.load(ui_images / 'Play_button.png')
    state = 'game'

    def __init__(self, x, y, size: tuple, num=-1):
        super().__init__(x, y, size)
        self.num = num


class ToMenu(GameChangeStateButton):
    image = pygame.image.load(ui_images / 'Exit_button.png')
    state = 'main_menu'


class QuitButton(GUI_trigger):
    image = pygame.image.load(ui_images / 'Exit_button.png')
    gui = Quit


class SettingsButton(GUI_trigger):
    image = pygame.image.load(ui_images / 'Settings_button.png')
    gui = SettingsWindow


class RetryButton(LevelQuitButton):
    next_level = False
    image = pygame.image.load(ui_images / 'Retry_button.png')


class NextLevelButton(LevelQuitButton):
    image = pygame.image.load(ui_images / 'Pause_button.png')


class TextButton(Button, Movable_UI):

    def __init__(self, x, y, size: tuple, end_pos: tuple, func_button: Button,
                 button_color, text: str, font=menu_font, color='black', delay=0):
        super().__init__(x, y, size, end_pos, delay)
        self.image.set_colorkey('yellow')
        self.image.fill('yellow')
        pygame.draw.rect(self.image, 'black',
                         (0, 0, self.rect.width, self.rect.height), border_radius=3)

        pygame.draw.rect(self.image, button_color,
                         (5, 5, self.rect.width - 10, self.rect.height - 10), border_radius=8)
        title = font.render(text, True, color)
        self.image.blit(title, ((self.rect.width - title.get_width()) // 2,
                                (self.rect.height - title.get_height()) // 2))
        self.func_button = func_button

    def move(self, speed=20) -> pygame.math.Vector2:
        super().move(speed)
        self.func_button.rect = self.rect


class UI_container(Movable_UI):  # menus, etc

    def __init__(self, x, y, size: tuple, content: list[UI], end_point: tuple):
        self.active = False
        super().__init__(x, y, size, end_point)
        self.content = content
        for ui in self.content:
            self.image.blit(ui.image, ui.rect.topleft)
            ui.rect.x += self.rect.x
            ui.rect.y += self.rect.y
        self.init_pos = self.rect.center
        self.end_pos = end_point

    def move(self, speed=20):
        move = super().move(speed)
        if move.length():
            for ui in self.content:
                ui.rect.move_ip(move)

    # TODO implement updating of containers like menus
    def update(self, **kwargs):
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
        super().draw(surface)


class EndLevelMenu(UI_container):
    image = pygame.image.load(ui_images / 'EndLevel_menu.png')

    def __init__(self, x, y, size: tuple, content: list[UI], end_point: tuple,
                 level_name: str, cur_time, max_score, player_score):
        super().__init__(x, y, size, content, end_point)
        self.image.blit(menu_font.render(level_name + " passed!", True, '#9C6409'), (160, 8))
        self.image.blit(menu_font.render('Time', True, '#9C6409'), (330, 120))
        self.init_pos = self.rect.center
        self.end_pos = end_point

        self.time = cur_time
        self.cur_score = 0
        self.player_score = player_score
        self.max_score = max_score

    def draw(self, surface: pygame.Surface, speed=20):
        if self.cur_score < self.player_score:
            self.cur_score += 1

        pygame.draw.rect(self.image, '#eecc67', (85, 115, 170, 50))
        self.image.blit(menu_font.render(f'{self.cur_score} / {self.max_score}', True, '#9C6409'), (85, 115))

        pygame.draw.rect(self.image, '#B8B1A6', (480, 115, 110, 45))
        self.image.blit(menu_font.render(strftime('%M:%S', gmtime(self.time)), True, '#9C6409'),
                        (480, 115))
        super().draw(surface)


class LevelEnter(UI):
    requires_offset = True
    requires_player = True
    image = pygame.image.load(ui_images / 'Level_enter.png')

    def __init__(self, x, y, size, num, manager: GameManager):
        super().__init__(x, y, size)
        self.num = num
        self.manager = manager
        self.level_data = manager.get_level_info(num)

        self.active_zone = pygame.Rect(self.rect.x - self.rect.width, self.rect.y - self.rect.height,
                                       self.rect.width * 2, self.rect.height * 2)

        level_num = menu_font.render(str(num), True, 'black')
        self.image.blit(level_num,
                        ((self.image.get_width() - level_num.get_width()) // 2,
                         self.image.get_height() // 2))

    def draw(self, surface: pygame.Surface):
        super().draw(surface)

    def interact(self, player: Player):
        if self.active_zone.colliderect(player.rect):
            pass


class LevelStats(UI_container):
    image = pygame.image.load(ui_images / 'Level_stats.png')

    locked_level = pygame.image.load(ui_images / 'Locked_level.png')
    unlocked_level = pygame.image.load(ui_images / 'Level_stats.png')

    def __init__(self, x, y, size: tuple, content: list[UI], end_point: tuple):
        super().__init__(x, y, size, content, end_point)
        self.level_stats = {'locked': True, 'passed': False, 'best_time': float('inf'), 'best_score': -1, 'stars': 0}
        self.level_num = -1

    def update(self, level_num, level_stats: dict):
        self.level_stats.update(level_stats)
        if level_stats['locked']:
            self.image.blit(self.locked_level, (0, 0))

        elif not level_stats['passed']:
            self.image.blit(self.unlocked_level, (0, 0))
            for ui in self.content:
                self.image.blit(ui.image, (ui.rect.x - self.rect.x, ui.rect.y - self.rect.y))
            level_name = info_font.render(f'Level {level_num}', True, 'black')
            best_time = info_font.render(f'Best time:-:-', True, 'black')
            best_score = info_font.render(f'Best score:-', True, 'black')
            pygame.draw.rect(self.image, '#eecc67', (30, 20, 200, 22))
            self.image.blit(level_name, (30, 20))
            pygame.draw.rect(self.image, '#eecc67', (30, 65, 500, 22))
            self.image.blit(best_time, (30, 65))
            pygame.draw.rect(self.image, '#eecc67', (30, 110, 200, 25))
            self.image.blit(best_score, (30, 110))

        else:
            self.image.blit(self.unlocked_level, (0, 0))
            for ui in self.content:
                self.image.blit(ui.image, (ui.rect.x - self.rect.x, ui.rect.y - self.rect.y))

            level_name = info_font.render(f'Level {level_num}', True, 'black')
            print(self.level_stats["best_time"] * 1000)
            best_time = info_font.render(f'Best time: {strftime("%M:%S", gmtime(round(self.level_stats["best_time"] * 1000)))}',
                                         True, 'black')
            best_score = info_font.render(f'Best score: {level_stats["best_score"]}',
                                         True, 'black')
            pygame.draw.rect(self.image, '#eecc67',  (30, 20, 200, 22))
            self.image.blit(level_name, (30, 20))
            pygame.draw.rect(self.image, '#eecc67', (30, 65, 500, 22))
            self.image.blit(best_time, (30, 65))
            pygame.draw.rect(self.image, '#eecc67', (30, 110, 250, 25))
            self.image.blit(best_score, (30, 110))


        self.level_num = level_num
        self.content[0].num = level_num
