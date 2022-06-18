from scripts.Drawing import *
from scripts.map_generation import *

display = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
pygame.display.set_caption('Pygame Platformer')

clock = pygame.time.Clock()

player = Player(100, 500)

drawing = Drawing(display)

level = generate_level(level_map)

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j:
                player.jump()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass

    drawing.background()
    player.draw(display)
    player.move()
    player.update()

    level.draw(display)
    level.physics([player])

    pygame.display.update()

    clock.tick(FPS)
