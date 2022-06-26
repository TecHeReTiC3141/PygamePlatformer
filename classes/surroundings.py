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

        elif entity.rect.colliderect(self.outer_rect):
            if entity.rect.right >= self.outer_rect.left >= entity.prev_rect.right:
                entity.collided_sides['right'] = True

            # right side
            elif entity.rect.left <= self.outer_rect.right <= entity.prev_rect.left:
                entity.collided_sides['left'] = True

    def draw(self, surface: pygame.Surface):
        surface.blit(self.surface, self.rect)

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


class MovingPlatform:

    def __init__(self, x, y, num_blocks, typ: str, dist, speed=5):
        self.init_point = pygame.math.Vector2(x, y)
        self.blocks: list[MovableBlock] = [MovableBlock(x + i, y) for i in range(num_blocks)]
        self.dist = dist
        self.typ = typ
        self.movement = pygame.math.Vector2(0 if typ == 'vert' else speed,
                                            0 if typ == 'hor' else speed)

    def collide(self, entity: Player):
        for block in self.blocks:
            block.collide(entity)

    def draw(self, surface: pygame.Surface):
        for block in self.blocks:
            block.draw(surface)

    def move(self):
        for block in self.blocks:
            block.rect.move_ip(self.movement)
            block.outer_rect.move_ip(self.movement)

        if self.typ == 'hor' and self.blocks[0].rect.left <= self.init_point.x \
                or self.blocks[1].rect.right >= self.init_point.x + self.dist:
            self.movement.x *= -1
        elif self.typ == 'vert' and self.blocks[0].rect.top <= self.init_point.y \
                    or self.blocks[-1].rect.bottom >= self.init_point.y + self.dist:
            self.movement.x *= -1

class Decor:

    def __init__(self, x, y, surface: pygame.Surface):
        width, height = surface.get_size()
        self.surface = pygame.transform.scale(surface.convert_alpha(),
                                              (width * SCALE, height * SCALE))
        self.rect = surface.get_rect(topleft=(x, y))

    def draw(self, surface: pygame.Surface):
        surface.blit(self.surface, self.rect)



