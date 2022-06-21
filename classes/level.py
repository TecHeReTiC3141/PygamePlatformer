from classes.surroundings import *


class Level:

    def __init__(self, walls: list[Block], moving_obj: list[MovingPlatform],
                 surface: pygame.Surface, start_pos: tuple[int, int]):
        self.walls = walls
        self.moving_obj = moving_obj
        self.surf = surface
        self.surf.set_colorkey('yellow')
        self.camera = Camera(surface)
        self.player = Player(*start_pos)

    def draw(self, surface: pygame.Surface):
        self.surf.fill('yellow')
        self.player.draw(self.surf)
        for wall in self.walls + self.moving_obj :
            wall.draw(self.surf)
        surface.blit(self.surf, (0, 0), self.camera.scroll(self.player))

    # TODO try to solve problem connected with collisions and movement
    def physics(self, entities: list[Player]):
        for plat in self.moving_obj:
            plat.move()
        for entity in entities:
            for wall in self.walls + self.moving_obj:
                wall.collide(entity)

    def game_cycle(self, surface: pygame.Surface):
        self.draw(surface)
        self.player.move()
        self.player.update()
        self.physics([self.player])
