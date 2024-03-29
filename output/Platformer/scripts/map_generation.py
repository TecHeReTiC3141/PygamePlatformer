from classes.level import *
from pytmx.util_pygame import load_pygame


# TODO add more levels (at least 6-7)
def gen_level(game_manager: GameManager, num: int) -> Level:
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

        if obj.type == 'Marker':
            if obj.name == 'Player':
                start_pos = (obj.x, obj.y)

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

        elif obj.type == 'Entity':
            if obj.name == 'GreenCannon':
                if obj.direction == 'up':
                    x, y = obj.x, obj.y
                elif obj.direction == 'down':
                    x, y = obj.x - obj.width, obj.y + obj.height
                elif obj.direction == 'right':
                    x, y = obj.x, obj.y + obj.height
                elif obj.direction == 'left':
                    x, y = obj.x - obj.height // 2, obj.y + obj.width // 2

                entities.append(Cannon(x, y, obj.width, obj.height,
                                       obj.direction, obj.max_dist, None, ))
                print(obj.x, obj.y, obj.width, obj.height)

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
                  decor, entities, surface, background_surf, start_pos, level_end, game_manager)
    return level
