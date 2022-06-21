from scripts.const import *
from pytmx.util_pygame import load_pygame

display = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
pygame.display.set_caption('Tiled test')

clock = pygame.time.Clock()

tiled_map = load_pygame('../resources/map/test_map.tmx')
TILE_SIZE = 128

ground_layer = tiled_map.get_layer_by_name('Ground')
print(ground_layer.width, ground_layer.height)
offset = [0, 0]

main_surf = pygame.Surface((TILE_SIZE * ground_layer.width,
                            TILE_SIZE * ground_layer.height))
for x, y, surf in ground_layer.tiles():
    main_surf.blit(surf, (x * 128, y * 128))
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    keys = pygame.mouse.get_pressed()
    if keys[1]:
        rel_x, rel_y = pygame.mouse.get_rel()
        offset[0] += rel_x
        offset[1] += rel_y
    display.fill('grey')
    display.blit(main_surf, (0, 0),
                 (offset[0], offset[1], DISP_WIDTH, DISP_HEIGHT))
    display.blit(info_font.render(f'{offset[0]}, {offset[1]}', True, 'black'), (30, 30))
    pygame.display.update()

    clock.tick(FPS)