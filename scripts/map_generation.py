from classes.level import *

def generate_level(map: list[str]) -> Level:

    walls: list[Block] = []
    for row in range(len(map)):
        for col in range(len(map[0])):
            if map[row][col] == '#':
                walls.append(Block(col, row))

    level = Level(walls)
    return level