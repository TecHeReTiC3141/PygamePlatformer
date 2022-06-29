from classes.player import *


class Block:
    movable = False

    def __init__(self, x, y, surface: pygame.Surface):
        self.surface = pygame.transform.scale(surface, (BLOCK_SIZE, BLOCK_SIZE))

        self.rect = self.surface.get_rect(topleft=(x * BLOCK_SIZE, y * BLOCK_SIZE))
        self.outer_rect = pygame.Rect(self.rect.left - 3, self.rect.top,
                                      self.rect.width + 6, self.rect.height)

    def collide(self, entity: Player, mode: str):

        if entity.rect.colliderect(self.rect):
            if mode == 'v':
                # left side
                if entity.velocity.x > 0:
                    entity.rect.right = self.rect.left
                    entity.collided_sides['right'] = True

                # right side
                elif entity.velocity.x < 0:
                    entity.rect.left = self.rect.right
                    entity.collided_sides['left'] = True

            elif mode == 'h':
                # top side
                if entity.velocity.y > 0:
                    entity.rect.bottom = self.rect.top
                    entity.collided_sides['down'] = True

                # bottom side
                elif entity.velocity.y < 0:
                    entity.rect.top = self.rect.bottom
                    entity.collided_sides['top'] = True


    def draw(self, surface: pygame.Surface):
        surface.blit(self.surface, self.rect)


class MovingPlatform(Block):

    def __init__(self, x, y, width, height, typ: str, dist, speed=5):
        self.init_point = pygame.math.Vector2(x, y)
        self.surface = pygame.Surface((width, height))
        self.surface.fill('blue')
        self.rect = self.surface.get_rect(topleft=(x, y))
        self.dist = dist * BLOCK_SIZE
        self.typ = typ
        self.movement = pygame.math.Vector2(0 if typ == 'vert' else speed,
                                            0 if typ == 'hor' else speed)

    def move(self):

        self.rect.move_ip(self.movement)
        if self.typ == 'hor' and (self.rect.left < self.init_point.x
                                  or self.rect.left > self.init_point.x + self.dist):
            self.movement *= -1
        elif self.typ == 'vert' and (self.rect.top < self.init_point.y
                                     or self.rect.top > self.init_point.y + self.dist):
            self.movement *= -1


class MovableBlock(Block):
    movable = True

    def __init__(self, x, y):
        surf = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        super().__init__(x, y, surf)
        self.weight = randint(1, 5)
        self.collided_size = {i: None for i in directions}
        self.surface.fill('green')

    def draw(self, surface: pygame.Surface):
        self.surface.fill('green')
        surface.blit(self.surface, self.rect)

    def check_walls(self, walls: list[Block]):
        pass

class GameObject:

    sprites: dict[int, pygame.Surface] = {}

    def __init__(self, x, y, width, height, surface: pygame.Surface):
        x, y, width, height = x * SCALE, y * SCALE, width * SCALE, height * SCALE
        self.surface = pygame.transform.scale(surface, (width, height)).convert_alpha()
        self.rect = self.surface.get_rect(topleft=(x, y))

    def draw(self, surface: pygame.Surface):
        surface.blit(self.surface, self.rect)

class Decor(GameObject):
    pass


class Text(Decor):
    pass


class LevelEnd(GameObject):
    # TODO improve appearance
    sprites = {0: 'resources/images/surrounding/door_closed.png',
               1: 'resources/images/surrounding/door_open.png'}

    def __init__(self, x, y, width, height, surface: pygame.Surface):
        super().__init__(x, y, width, height, surface)
        self.active_zone = pygame.Rect(self.rect.x - self.rect.width,
                                       self.rect.y - self.rect.height,
                                       self.rect.width * 2, self.rect.height * 2)
        self.active = False

    def update(self, player: Player) -> bool:
        self.active = 0
        if player.rect.colliderect(self.active_zone):
            print('active')
            self.active = 1
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_o:
                    return True
        return False

