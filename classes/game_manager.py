from scripts.const import *
from scripts.generate_level_stats import *


class GameManager:

    def __init__(self, display: pygame.Surface, res=(DISP_WIDTH, DISP_HEIGHT)):
        self.game_state = 'main_menu'
        self.display = display
        self.is_paused = False
        self.difficulty = 'Medium'
        self.surf = pygame.Surface(res)
        self.clock = pygame.time.Clock()

        # settings
        self.cursor_color = tuple(randint(0, 255) for _ in '...')

        self.__level_stats = get_level_stats()

        self.__config = {
            'res': res,
            'show_debug': True,
            'particles': True
        }

    # TODO implement updating of level_stats.json when game is quited
    def __del__(self):
        pass

    def change_state(self, new_state):
        pass

    @property
    def res(self):
        return self.__config['res']

    @property
    def show_debug(self):
        return self.__config['show_debug']

    @property
    def particles(self):
        return self.__config['particles']

    def get_level_info(self, idx):
        return self.__level_stats.get(f'level{idx}', {})

    def update_level(self, idx, level_data):
        self.__level_stats[f'level{idx}'].update(level_data)

    def update(self, fullscreen: bool, **new_config: dict):
        if fullscreen:
            self.display = pygame.display.set_mode(new_config['res'], pygame.FULLSCREEN)
        else:
            self.display = pygame.display.set_mode(new_config['res'])
        self.__config.update(new_config)
