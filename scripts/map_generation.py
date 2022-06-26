from classes.level import *
from pytmx.util_pygame import load_pygame

# TODO create level borders to prevent player from falling
def gen_level(path: str) -> Level:
    level_map = load_pygame(f'levels/{path}.tmx')

    obj_layer = level_map.get_layer_by_name('GameObjects')
    blocks = level_map.get_layer_by_name('BlocksLayer')

    start_pos = (0, 0)
    decor: list[Decor] = []
    for obj in obj_layer:
        if obj.type == 'Marker':
            if obj.name == 'Player':
                start_pos = (obj.x * BLOCK_SIZE // 128, obj.y * BLOCK_SIZE // 128)
    #     elif obj.type == 'Decor':
    #         print(obj.name, obj.image)
    #         decor.append(Decor(obj.x * BLOCK_SIZE // 128, obj.y * BLOCK_SIZE // 128, obj.image))
    # print(start_pos)

    surface = pygame.Surface((level_map.width * BLOCK_SIZE,
                              level_map.height * BLOCK_SIZE))

    walls: list[Block] = []
    for x, y, surf in blocks.tiles():
        walls.append(Block(x, y, surf))

    level = Level(walls, [], decor, surface, start_pos)
    return level