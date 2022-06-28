from classes.level import *
from pytmx.util_pygame import load_pygame


def gen_level(path: str) -> Level:
    level_map = load_pygame(f'levels/{path}.tmx')

    obj_layer = level_map.get_layer_by_name('GameObjects')
    blocks = level_map.get_layer_by_name('BlocksLayer')

    start_pos = (0, 0)
    decor: list[Decor] = []
    moving_objs: list[MovingPlatform] = []

    # Loading objects
    for obj in obj_layer:
        if obj.type == 'Marker':
            if obj.name == 'Player':
                start_pos = (round(obj.x * SCALE), round(obj.y * SCALE))

        elif obj.type == 'Decor':
            decor.append(Decor(round(obj.x * SCALE), round(obj.y * SCALE), obj.image))

        elif obj.type == 'MovingPlatform':
            moving_objs.append(MovingPlatform(obj.x * SCALE, obj.y * SCALE, obj.width * SCALE, obj.height * SCALE,
                                              obj.typ, obj.dist, obj.speed))

    surface = pygame.Surface((level_map.width * BLOCK_SIZE,
                              level_map.height * BLOCK_SIZE))

    # Loading blocks
    walls: list[Block] = []
    for x, y, surf in blocks.tiles():
        walls.append(Block(x, y, surf))

    level = Level(walls, moving_objs, decor, surface, start_pos)
    return level