from scripts.map_generation import *
from classes.drawing import Drawing

display = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT), 0, 42)
pygame.display.set_caption('Pygame Platformer')
pygame.display.set_icon(pygame.transform.scale(pygame.image.load('ico_player.ico'),
                                               (32, 32)))

tick = 0
game_manager = GameManager(display)
level = MainMenu(game_manager)
drawing = Drawing(game_manager, level)

# TODO implement console for debugging
while True:
    delta = game_manager.clock.tick(FPS) * .001 * FPS

    drawing.draw()

    if game_manager.game_state == 'main_menu':
        to_level = level.game_cycle(delta)
        if to_level is not None:
            level = gen_level(game_manager, randint(1, 6))
            game_manager.game_state = 'game'

    elif game_manager.game_state == 'game':
        end_level = level.game_cycle(delta)
        if end_level is not None:
            level = gen_level(game_manager, level.num + end_level)
            drawing.level = level

    pygame.display.update()

    tick += 1
    if not tick % FPS:
        pass
