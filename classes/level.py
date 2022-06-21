from classes.surroundings import *


class Level:

    def __init__(self, walls: list[Block], moving_obj: list[MovingPlatform],
                 surface: pygame.Surface):
        self.walls = walls
        self.moving_obj = moving_obj
        self.surf = surface
        self.surf.set_colorkey('yellow')
        self.camera = Camera(surface)

    def draw(self, surface: pygame.Surface, player: Player):
        self.surf.fill('yellow')
        player.draw(self.surf)
        for wall in self.walls + self.moving_obj :
            wall.draw(self.surf)
        surface.blit(self.surf, (0, 0), self.camera.scroll(player))

    def physics(self, entities: list[Player]):
        for entity in entities:
            for wall in self.walls + self.moving_obj:
                wall.collide(entity)
