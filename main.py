from scripts.Drawing import *
from scripts.map_generation import *

display = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
pygame.display.set_caption('Pygame Platformer')


clock = pygame.time.Clock()
tick = 0

player = Player(100, 0)

drawing = Drawing(display)

level = generate_level('level1')

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass

    drawing.background()
    level.draw(display, player)

    player.move()
    player.update()

    level.physics([player])

    pygame.display.update()

    clock.tick(FPS)
    tick += 1
    if not tick % FPS:
        pass
        #print(player.collided_sides)
