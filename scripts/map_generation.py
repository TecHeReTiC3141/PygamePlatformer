from classes.level import *
from pytmx.util_pygame import load_pygame

# TODO add more levels (at least 6-7)
def gen_level(num: int) -> Level:
    path = 'level' + str(num)
    level_map = load_pygame(f'levels/{path}.tmx')

    obj_layer = level_map.get_layer_by_name('GameObjects')
    blocks = level_map.get_layer_by_name('BlocksLayer')

    start_pos = (0, 0)
    decor: list[Decor] = []
    moving_objs: list[MovingPlatform] = []

    level_end: LevelEnd = None
    # Loading objects
    for obj in obj_layer:
        print(obj.type, obj.name, obj.x, obj.y,obj.width, obj.height, obj.image)
        if obj.type == 'Marker':
            if obj.name == 'Player':
                start_pos = (round(obj.x * SCALE), round(obj.y * SCALE))

        elif obj.type == 'Decor':
            decor.append(Decor(obj.x, obj.y,obj.width, obj.height, obj.image,))
        #
        # elif obj.type == 'Text':
        #     print(obj.__dict__)
        #     decor.append(Text(obj.x, obj.y, obj.width, obj.height, obj.image, ))

        elif obj.type == 'MovingPlatform':
            moving_objs.append(MovingPlatform(obj.x * SCALE, obj.y * SCALE, obj.width * SCALE,
                                              obj.height * SCALE, obj.typ, obj.dist, obj.speed))

        elif obj.type == 'LevelEnd':
            level_end = LevelEnd(obj.x, obj.y, obj.width, obj.height, obj.image)
            print(level_end)

    surface = pygame.Surface((level_map.width * BLOCK_SIZE,
                              level_map.height * BLOCK_SIZE))

    assert isinstance(level_end, LevelEnd), "No LevelEnd"
    # Loading blocks
    walls: list[Block] = []
    for x, y, surf in blocks.tiles():
        walls.append(Block(x, y, surf))

    level = Level(num, walls, moving_objs, decor, surface, start_pos, level_end)
    return level