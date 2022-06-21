from classes.level import *

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