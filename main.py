from scripts.map_generation import *

display = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT), 0, 42)
pygame.display.set_caption('Pygame Platformer')

clock = pygame.time.Clock()
tick = 0
game_manager = GameManager()
level = gen_level(game_manager, 5)
drawing = Drawing(display, level)

while True:
    delta = clock.tick(FPS) * .001 * FPS

    drawing.draw()

    end_level = level.game_cycle(delta)
    if end_level:
        level = gen_level(game_manager, level.num + 1)
        drawing.level = level

    pygame.display.update()

    tick += 1
    if not tick % FPS:
        pass
