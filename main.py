from scripts.Drawing import *
from scripts.map_generation import *

display = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
pygame.display.set_caption('Pygame Platformer')

clock = pygame.time.Clock()
tick = 0

drawing = Drawing(display)

level = gen_level('level1')
# level.moving_obj.append(MovingPlatform(1, 5, 4, 'hor', 450))

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                level.player.jump()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass

    drawing.background()

    level.game_cycle(display)

    pygame.display.update()

    clock.tick(FPS)
    tick += 1
    if not tick % FPS:
        pass
        # print(player.collided_sides)
