from classes.surroundings import *


class Level:

    def __init__(self, walls: list[Block], moving_obj: list[MovingPlatform],
                 surface: pygame.Surface, start_pos: tuple[int, int]):
        self.blocks = walls
        self.moving_obj: list[MovingPlatform] = moving_obj
        self.surf = surface
        self.surf.set_colorkey('yellow')
        self.camera = Camera(surface)
        self.projectiles: list[Projectile] = []
        self.player = Player(*start_pos)

    def draw(self, surface: pygame.Surface):
        self.surf.fill('yellow')
        self.player.draw(self.surf)
        for obj in self.blocks + self.moving_obj + self.projectiles:
            obj.draw(self.surf)

        surface.blit(self.surf, (0, 0), self.camera.scroll(self.player))

    # TODO try to solve problem connected with collisions and movement
    def physics(self, entities: list[Player]):
        for plat in self.moving_obj:
            plat.move()

        for proj in self.projectiles:
            proj.move()
            for block in self.blocks:
                proj.collide(block)

        for entity in entities:
            for wall in self.blocks + self.moving_obj:
                wall.collide(entity)

    def game_cycle(self, surface: pygame.Surface):
        self.draw(surface)
        surface.blit(info_font.render(str(round(degrees(self.player.angle))), True, 'black'),
                     (30, 30))

        self.player.move()
        self.player.get_angle(self.camera.offset)
        self.player.update()
        self.physics([self.player])
        self.clear()

    def clear(self):
        self.projectiles = list(filter(lambda i: not i.collided,
                                       self.projectiles))
