from scripts.Drawing import *
from classes.surroundings import *
from scripts.map_generation import *

display = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
pygame.display.set_caption('Pygame Platformer')

clock = pygame.time.Clock()

player = Player(100, 100)

drawing = Drawing(display)

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            pass

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass

    drawing.background()
    player.draw(display)
    player.move()

    pygame.display.update()

    clock.tick(FPS)
