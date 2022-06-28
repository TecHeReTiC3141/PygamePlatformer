from scripts.Drawing import *
from scripts.map_generation import *

display = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT), 0, 42)
pygame.display.set_caption('Pygame Platformer')

clock = pygame.time.Clock()
tick = 0

drawing = Drawing(display)

level = gen_level('level3')


while True:
    delta = clock.tick(FPS) * .001 * FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                level.player.jump()

            elif event.key == pygame.K_e:
                level.projectiles.append(level.player.shoot())

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass

    drawing.background()

    level.game_cycle(display, delta)

    pygame.display.update()

    tick += 1
    if not tick % FPS:
        pass
        # print(player.collided_sides)
