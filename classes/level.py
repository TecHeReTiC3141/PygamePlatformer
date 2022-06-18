from classes.surroundings import *

class Level:

    def __init__(self, walls: list[Block]):
        self.walls = walls

    def draw(self, surface: pygame.Surface):
        for wall in self.walls:
            wall.draw(surface)

    def physics(self, entities: list[Player]):
        for entity in entities:
            for wall in self.walls:
                wall.collide(entity)

