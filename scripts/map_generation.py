from classes.level import *
from pytmx.util_pygame import load_pygame


# TODO add more levels (at least 6-7)
def gen_level(game_manager: GameManager, num: int) -> Level:
    path = 'level' + str(num)
    level_map = load_pygame(f'levels/{path}.tmx')

    obj_layer = level_map.get_layer_by_name('GameObjects')
    blocks_layer = level_map.get_layer_by_name('BlocksLayer')
    background = level_map.get_layer_by_name('BackGround')

    decor: list[Decor] = []
    obstacles: list[Obstacle] = []
    collectable: list[Collectable] = []
    entities: list[Entity] = []
    blocks: list[Block] = []

    key_count = 0
    start_pos: tuple = None
    level_end: LevelEnd = None

    surface = pygame.Surface((level_map.width * BLOCK_SIZE,
                              level_map.height * BLOCK_SIZE))

    background_surf = pygame.Surface((level_map.width * BLOCK_SIZE,
                                      level_map.height * BLOCK_SIZE))

    for x, y, surf in background.tiles():
        background_surf.blit(surf, (x * BLOCK_SIZE, y * BLOCK_SIZE))

    # Loading objects
    for obj in obj_layer:

        if obj.type == 'Marker':
            if obj.name == 'Player':
                start_pos = (obj.x, obj.y)

            elif obj.name == 'Text':
                background_surf.blit(stats_font.render(obj.text, True, obj.color),
                                     (obj.x * SCALE, obj.y * SCALE))
        #
        # elif obj.type == 'Decor':
        #     decor.append(Decor(obj.x, obj.y, obj.width, obj.height, obj.image, ))

        elif obj.type == 'Money':
            collectable.append(Coin(obj.x, obj.y, obj.width, obj.height, obj.image))

        elif obj.type == 'Key':
            collectable.append(Key(obj.x, obj.y, obj.width, obj.height, obj.image))
            key_count += 1

        elif obj.type == 'MovingPlatform':
            obstacles.append(MovingPlatform(obj.x, obj.y, obj.width,
                                            obj.height, obj.image, obj.typ, obj.dist, obj.speed))

        elif obj.type == 'Spike':
            obstacles.append(Spike(obj.x, obj.y, obj.width,
                                   obj.height, obj.image))

        elif obj.type == 'LevelEnd':
            level_end = LevelEnd(obj.x, obj.y, obj.width, obj.height, obj.image, key_count)

        elif obj.name == 'Water':
            obstacles.append(Water(obj.x, obj.y, obj.width, obj.height, obj.image))

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
                # print(obj.x, obj.y, obj.width, obj.height)

    assert isinstance(level_end, LevelEnd), "No LevelEnd"
    assert isinstance(start_pos, tuple), "No player"

    # Loading blocks
    for x, y, surf in blocks_layer.tiles():
        blocks.append(Block(x, y, surf))

    level = Level(num, blocks, obstacles, collectable,
                  decor, entities, surface, background_surf, start_pos, key_count, level_end, game_manager)
    return level


def gen_main_menu(game_manager: GameManager) -> MainMenu:
    menu_level = load_pygame(f'levels/main_menu.tmx')

    obj_layer = menu_level.get_layer_by_name('GameObjects')
    blocks = menu_level.get_layer_by_name('BlocksLayer')

    surface = pygame.Surface((menu_level.width * BLOCK_SIZE,
                              menu_level.height * BLOCK_SIZE))
    surface.fill('#3eb5e4')
    for x, y, surf in blocks.tiles():
        surface.blit(pygame.transform.scale(surf, (BLOCK_SIZE, BLOCK_SIZE)), (x * BLOCK_SIZE, y * BLOCK_SIZE))

    for obj in obj_layer:
        print(obj.x, obj.y)
        surface.blit(pygame.transform.scale(obj.image, (obj.width, obj.height)),
                     (obj.x * SCALE, (obj.y - obj.height) * SCALE))

    return MainMenu(game_manager, surface)


def gen_levels_map(game_manager: GameManager) -> LevelMap:
    level_map = load_pygame(f'levels/level_map.tmx')

    game_objs = level_map.get_layer_by_name('GameObjects')
    blocks_layer = level_map.get_layer_by_name('BlocksLayer')
    background = level_map.get_layer_by_name('BackGround')

    background_surface = pygame.Surface((level_map.width * BLOCK_SIZE,
                                         level_map.height * BLOCK_SIZE))
    surface = pygame.Surface((level_map.width * BLOCK_SIZE,
                              level_map.height * BLOCK_SIZE))
    water_coords = [(x, y) for x in range(level_map.width)
                    for y in range(level_map.height)]

    for x, y, surf in background.tiles():
        background_surface.blit(pygame.transform.scale(surf, (BLOCK_SIZE, BLOCK_SIZE)),
                                (x * BLOCK_SIZE, y * BLOCK_SIZE))
        water_coords.remove((x, y))

    start_pos: tuple = None
    enters: list[LevelEnter] = []
    obstacles: list[Obstacle] = []

    for x, y in water_coords:
        obstacles.append(SolidWater(x * level_map.tilewidth, y * level_map.tileheight, BLOCK_SIZE, BLOCK_SIZE,
                                    pygame.Surface((level_map.tilewidth, level_map.tileheight))))

    for obj in game_objs:

        if obj.type == 'Player':
            start_pos = (obj.x, obj.y)
        elif obj.type == 'Level':
            enters.append(LevelEnter(obj.x * SCALE, obj.y * SCALE, (obj.width, obj.height),
                                     int(obj.name), game_manager))

    return LevelMap(obstacles, enters, surface,
                    background_surface, start_pos, game_manager)
