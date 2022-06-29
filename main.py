from scripts.Drawing import *
from scripts.map_generation import *

display = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT), 0, 42)
pygame.display.set_caption('Pygame Platformer')

clock = pygame.time.Clock()
tick = 0

drawing = Drawing(display)

level = gen_level('level2')


while True:
    delta = clock.tick(FPS) * .001 * FPS

    drawing.background()

    level.game_cycle(display, delta)

    pygame.display.update()

    tick += 1
    if not tick % FPS:
        pass
        # print(player.collided_sides)
