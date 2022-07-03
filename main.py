from scripts.map_generation import *

display = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT), 0, 42)
pygame.display.set_caption('Pygame Platformer')

clock = pygame.time.Clock()
tick = 0

level = gen_level(2)
drawing = Drawing(display, level)

while True:
    delta = clock.tick(FPS) * .001 * FPS

    drawing.draw()

    end_level = level.game_cycle(display, delta)
    if end_level:
        level = gen_level(level.num + 1)

    pygame.display.update()

    tick += 1
    if not tick % FPS:
        pass
