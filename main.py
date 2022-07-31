from scripts.map_generation import *
from classes.drawing import Drawing

display = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT), 0, 42)
pygame.display.set_caption('Pygame Platformer')
pygame.display.set_icon(pygame.transform.scale(pygame.image.load('ico_player.ico'),
                                               (32, 32)))

game_manager = GameManager(display)
level = MainMenu(game_manager)
drawing = Drawing(game_manager, level)

# TODO implement console for debugging
while True:
    delta = game_manager.clock.tick(FPS) * .001 * FPS

    drawing.draw()

    if game_manager.game_state == 'main_menu':
        to_level = level.game_cycle(delta)
        if isinstance(to_level, ToLevels):
            level = gen_level(game_manager, randint(1, 6))
            game_manager.game_state = 'game'
            drawing.level = level

    elif game_manager.game_state == 'game':
        cyc = level.game_cycle(delta)
        if isinstance(cyc, ToMenu):
            level = MainMenu(game_manager)
            drawing.level = level
            game_manager.game_state = 'main_menu'

        elif isinstance(cyc, LevelQuitButton):
            level = gen_level(game_manager, level.num + cyc.next_level)
            drawing.level = level

    pygame.display.update()
