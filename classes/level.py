from classes.surroundings import *

class Camera:

    def __init__(self, surf: pygame.Surface):
        self.surf = surf
        self.offset = pygame.math.Vector2(0, 0)
        self.display_size = pygame.math.Vector2(DISP_WIDTH, DISP_HEIGHT)

    def scroll(self, player: Player) -> tuple:
        self.offset.x = min(max(0, player.rect.centerx - self.display_size.x // 2),
                            self.surf.get_width() - self.display_size.x)
        self.offset.y = min(max(0, player.rect.centery - self.display_size.y // 2),
                            self.surf.get_height() - self.display_size.y)
        return self.offset.x, self.offset.y, self.display_size.x, self.display_size.y

class Level:

    def __init__(self, walls: list[Block], moving_obj: list[MovingPlatform], decor: list[Decor],
                 surface: pygame.Surface, start_pos: tuple[int, int]):
        self.blocks = walls
        self.moving_obj: list[MovingPlatform] = moving_obj
        self.decor = decor
        self.surf = surface
        self.surf.set_colorkey('yellow')
        self.camera = Camera(surface)
        self.projectiles: list[Projectile] = []
        self.player = Player(*start_pos)

    def draw(self, surface: pygame.Surface):
        self.surf.fill('yellow')
        self.player.draw(self.surf)
        for obj in self.blocks + self.moving_obj + self.projectiles + self.decor:
            obj.draw(self.surf)

        surface.blit(self.surf, (0, 0), self.camera.scroll(self.player))

    # TODO try to solve problem connected with collisions and movement
    def physics(self, entities: list[Player], dt):
        for plat in self.moving_obj:
            plat.move()

        for proj in self.projectiles:
            proj.move()
            for block in self.blocks:
                proj.collide(block)

        if dt <= 3:
            for entity in entities:
                entity.vert_move(dt)
                for wall in self.blocks:
                    wall.collide(entity, 'h')
                entity.hor_move(dt)
                for wall in self.blocks:
                    wall.collide(entity, 'v')

    def game_cycle(self, surface: pygame.Surface, dt):
        self.draw(surface)
        surface.blit(info_font.render(str(round(degrees(self.player.angle))), True, 'black'),
                     (30, 30))

        self.player.get_angle(self.camera.offset)
        self.physics([self.player], dt)
        self.player.update(dt)

        self.clear()

    def clear(self):
        self.projectiles = list(filter(lambda i: not i.collided,
                                       self.projectiles))
