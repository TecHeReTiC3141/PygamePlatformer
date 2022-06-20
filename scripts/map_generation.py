from classes.level import *

generation_types = {
    '1': Block,
    '2': MovableBlock,
}

def generate_level(path: str) -> Level:
    with open(f'levels/{path}.txt') as f:
        map = [i.strip() for i in f.readlines()]
    walls: list[Block] = []
    surface = pygame.Surface((len(map[0]) * BLOCK_SIZE, len(map) * BLOCK_SIZE))
    print(surface)
    for row in range(len(map)):
        for col in range(len(map[0])):
            if map[row][col] != '.':
                walls.append((generation_types[map[row][col]])(col, row))

    level = Level(walls, surface)
    return level