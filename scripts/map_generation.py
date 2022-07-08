from classes.level import *
from pytmx.util_pygame import load_pygame


# TODO add more levels (at least 6-7)
# TODO entities to level
def gen_level(num: int) -> Level:
    path = 'level' + str(num)
    level_map = load_pygame(f'levels/{path}.tmx')

    obj_layer = level_map.get_layer_by_name('GameObjects')
    blocks = level_map.get_layer_by_name('BlocksLayer')
    background = level_map.get_layer_by_name('BackGround')

    start_pos = (0, 0)
    decor: list[Decor] = []
    obstacles: list[Obstacle] = []
    collectable: list[Collectable] = []
    entities: list[Entity] = []

    level_end: LevelEnd = None
    # Loading objects
    for obj in obj_layer:
        print(obj.type, obj.name, obj.x, obj.y, obj.width, obj.height, obj.image)
        if obj.type == 'Marker':
            if obj.name == 'Player':
                start_pos = (obj.x * SCALE, obj.y)

        elif obj.type == 'Decor':
            decor.append(Decor(obj.x, obj.y, obj.width, obj.height, obj.image, ))

        elif obj.type == 'Money':
            collectable.append(Coin(obj.x, obj.y, obj.width, obj.height, obj.image))

        elif obj.type == 'MovingPlatform':
            obstacles.append(MovingPlatform(obj.x, obj.y, obj.width,
                                            obj.height, obj.image, obj.typ, obj.dist, obj.speed))

        elif obj.type == 'Spike':
            obstacles.append(Spike(obj.x, obj.y, obj.width,
                                   obj.height, obj.image))

        elif obj.type == 'LevelEnd':
            level_end = LevelEnd(obj.x, obj.y, obj.width, obj.height, obj.image)
            print(level_end)

        elif obj.type == 'Entity':
            if obj.name == 'GreenCannon':
                entities.append(Cannon(obj.x, obj.y, obj.width, obj.height,
                                       obj.direction))

    surface = pygame.Surface((level_map.width * BLOCK_SIZE,
                              level_map.height * BLOCK_SIZE))

    background_surf = pygame.Surface((level_map.width * BLOCK_SIZE,
                                      level_map.height * BLOCK_SIZE))
    assert isinstance(level_end, LevelEnd), "No LevelEnd"
    # Loading blocks
    walls: list[Block] = []
    for x, y, surf in blocks.tiles():
        walls.append(Block(x, y, surf))

    for x, y, surf in background.tiles():
        background_surf.blit(surf, (x * BLOCK_SIZE, y * BLOCK_SIZE))

    level = Level(num, walls, obstacles, collectable,
                  decor, entities, surface, background_surf, start_pos, level_end)
    return level
