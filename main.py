from scripts.map_generation import *
from classes.drawing import Drawing

display = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT), 0, 42)
pygame.display.set_caption('Pygame Platformer')
pygame.display.set_icon(pygame.transform.scale(pygame.image.load('ico_player.ico'),
                                               (32, 32)))
pygame.mouse.set_visible(False)

game_manager = GameManager(display)
level = gen_main_menu(game_manager)
drawing = Drawing(game_manager, level)

# TODO implement console for debugging
if __name__ == '__main__':
    while True:
        delta = game_manager.clock.tick(FPS) * .001 * FPS

        drawing.draw()

        if game_manager.game_state == 'main_menu':
            to_levelmap = level.game_cycle(delta)
            if isinstance(to_levelmap, ToLevelMap):
                level = gen_levels_map(game_manager)
                game_manager.game_state = 'level_map'
                drawing.level = level

        elif game_manager.game_state == 'level_map':
            to_level = level.game_cycle(delta)
            if isinstance(to_level, LevelEnter):
                level = gen_level(game_manager, to_level.num)
                game_manager.game_state = 'game'
                drawing.level = level
            elif isinstance(to_level, ToMenu):
                level = gen_main_menu(game_manager)
                drawing.level = level
                game_manager.game_state = 'main_menu'

        elif game_manager.game_state == 'game':
            cyc = level.game_cycle(delta)
            if isinstance(cyc, ToMenu):
                level = gen_main_menu(game_manager)
                drawing.level = level
                game_manager.game_state = 'main_menu'

            elif isinstance(cyc, LevelQuitButton):
                level = gen_level(game_manager, level.num + cyc.next_level)
                drawing.level = level

        pygame.display.update()
