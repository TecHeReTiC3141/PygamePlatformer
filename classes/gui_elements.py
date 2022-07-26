import PySimpleGUI as sg
import pygame

from classes.game_manager import *

# TODO revise pysimplegui and implement Settings Window
class Window:
    layout = [[]]

    def __init__(self, game_manager: GameManager, win_name: str, theme='DarkAmber', ):
        self.manager = game_manager
        self.manager.is_paused = True
        sg.theme(theme)
        sg.set_options(font='Frank 12')

        self.window = sg.Window(win_name, self.layout, finalize=True)
        self.run()

    def run(self):
        pass

    def close(self):
        self.window.close()
        self.manager.is_paused = False
        print('closed')


class SettingsWindow(Window):

    def __init__(self, game_manager: GameManager, theme='DarkAmber', ):
        graphics_tab = sg.Tab('Graphics', [
            [sg.Frame('Game', [
                [sg.Spin(['Low', 'Medium', 'Hard'], initial_value=game_manager.difficulty,
                         text_color='red', key='-DIFFICULTY-',
                         tooltip='Defines damage from enemies and speed of hostile rockets')]
            ])],
            [sg.HorizontalSeparator()],
            [sg.Frame('Graphics', [
                [sg.Text('Resolution'), sg.Spin(['900x600', '1080x720', '1440x900'],
                                                initial_value='1440x900', key='-RES-'),
                 sg.Checkbox('Fullscreen', key='-FULLSCREEN-'), sg.Checkbox('Show damage', key='-DAMAGEIND-')]
            ], )]
        ], expand_y=True, expand_x=True)

        sound_tab = sg.Tab('Sounds', [
            [sg.Frame('Sounds', [
                [sg.Slider((1, 10), key='-SOUNDVOL', orientation='h', default_value=5)]
            ], expand_y=True, expand_x=True)],

            [sg.Frame('Music', [
                [sg.Slider((1, 10), key='-MUSICVOL', orientation='h', default_value=5)]
            ], expand_y=True, expand_x=True)]
        ])

        self.layout = [
            [sg.TabGroup([
                [graphics_tab, sound_tab],
            ])],
            [sg.HorizontalSeparator()],
            [sg.Push(), sg.Button('Reset', button_color='red'), sg.Button('Apply', button_color='green')]
        ]

        super().__init__(game_manager, 'Settings', theme)

    def run(self):

        while True:
            event,  values = self.window.read()
            if event == sg.WINDOW_CLOSED or event == 'Reset':
                break

            elif event == 'Apply':
                pass
                # self.manager.update()

        self.close()

game_manager = GameManager(pygame.Surface((DISP_WIDTH, DISP_HEIGHT)))
SettingsWindow(game_manager)