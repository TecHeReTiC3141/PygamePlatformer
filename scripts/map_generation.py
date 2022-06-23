from classes.level import *
from pytmx.util_pygame import load_pygame

generation_types = {
    '1': Block,
    '2': MovableBlock,
}

def generate_level(path: str) -> Level:
    with open(f'levels/{path}.txt') as f:
        level_map = [i.strip() for i in f.readlines()]
    start_pos = tuple(map(int, level_map.pop().split()))
    walls: list[Block] = []
    surface = pygame.Surface((len(level_map[0]) * BLOCK_SIZE, len(level_map) * BLOCK_SIZE))
    for row in range(len(level_map)):
        for col in range(len(level_map[0])):

            if level_map[row][col] != '.':
                walls.append((generation_types[level_map[row][col]])(col, row))

    level = Level(walls, [], surface, start_pos)
    return level

def gen_level(path: str) -> Level:
    level_map = load_pygame(f'levels/{path}.tmx')

    obj_layer = level_map.get_layer_by_name('GameObjects')
    blocks = level_map.get_layer_by_name('BlocksLayer')

    start_pos = (0, 0)
    for obj in obj_layer:
        if obj.type == 'Marker':
            if obj.name == 'Player':
                start_pos = (obj.x * BLOCK_SIZE // 128, obj.y * BLOCK_SIZE // 128)
    print(start_pos)

    surface = pygame.Surface((level_map.width * BLOCK_SIZE,
                              level_map.height * BLOCK_SIZE))

    walls: list[Block] = []
    for x, y, surf in blocks.tiles():
        walls.append(Block(x, y, surf))

    level = Level(walls, [], surface, start_pos)
    return level