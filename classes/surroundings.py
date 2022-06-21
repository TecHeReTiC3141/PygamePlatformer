from classes.player import *


class Block:
    surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
    movable = False

    def __init__(self, x, y):

        self.cur_rect = self.surface.get_rect(topleft=(x * BLOCK_SIZE, y * BLOCK_SIZE))
        self.outer_rect = pygame.Rect(self.cur_rect.left - 3, self.cur_rect.top,
                                      self.cur_rect.width + 6, self.cur_rect.height)
        self.surface.fill('blue')

    def collide(self, entity: Player):

        if entity.cur_rect.colliderect(self.cur_rect):

            # left side
            if entity.cur_rect.right >= self.cur_rect.left >= entity.prev_rect.right:
                entity.cur_rect.right = self.cur_rect.left
                entity.collided_sides['right'] = True

            # right side
            elif entity.cur_rect.left <= self.cur_rect.right <= entity.prev_rect.left:
                entity.cur_rect.left = self.cur_rect.right
                entity.collided_sides['left'] = True

            # top side
            if entity.cur_rect.bottom >= self.cur_rect.top >= entity.prev_rect.bottom:
                entity.cur_rect.bottom = self.cur_rect.top
                entity.collided_sides['down'] = True

            # bottom side
            elif entity.cur_rect.top <= self.cur_rect.bottom <= entity.prev_rect.top:
                entity.cur_rect.top = self.cur_rect.bottom
                entity.collided_sides['top'] = True

        elif entity.cur_rect.colliderect(self.outer_rect):
            if entity.cur_rect.right >= self.outer_rect.left >= entity.prev_rect.right:
                entity.collided_sides['right'] = True

            # right side
            elif entity.cur_rect.left <= self.outer_rect.right <= entity.prev_rect.left:
                entity.collided_sides['left'] = True

    def draw(self, surface: pygame.Surface):
        surface.blit(self.surface, self.cur_rect)

class MovableBlock(Block):

    movable = True

    def __init__(self, x, y):
        super().__init__(x, y)
        self.weight = randint(1, 5)
        self.collided_size = {i: None for i in directions}
        self.surface.fill('green')


    def collide(self, entity: Player):
        if entity.cur_rect.colliderect(self.cur_rect):
            movable = pygame.math.Vector2(0, 0)
            # left side
            if entity.cur_rect.right >= self.cur_rect.left >= entity.prev_rect.right:
                entity.cur_rect.right = self.cur_rect.left
                entity.collided_sides['right'] = True

            # right side
            elif entity.cur_rect.left <= self.cur_rect.right <= entity.prev_rect.left:
                entity.cur_rect.left = self.cur_rect.right
                entity.collided_sides['left'] = True

            # top side
            if entity.cur_rect.bottom >= self.cur_rect.top >= entity.prev_rect.bottom:
                entity.cur_rect.bottom = self.cur_rect.top
                entity.collided_sides['down'] = True

            # bottom side
            elif entity.cur_rect.top <= self.cur_rect.bottom <= entity.prev_rect.top:
                entity.cur_rect.top = self.cur_rect.bottom
                entity.collided_sides['top'] = True

        elif entity.cur_rect.colliderect(self.outer_rect):
            if entity.cur_rect.right >= self.outer_rect.left >= entity.prev_rect.right:
                entity.collided_sides['right'] = True

            # right side
            elif entity.cur_rect.left <= self.outer_rect.right <= entity.prev_rect.left:
                entity.collided_sides['left'] = True

    def check_walls(self, walls: list[Block]):
        pass


class MovingPlatform(Block):

    def __init__(self, x, y, num_blocks, typ: str, dist, speed=5):
        super().__init__(x, y)
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
            block.cur_rect.move_ip(self.movement)
            block.outer_rect.move_ip(self.movement)
            print(block.cur_rect)

        if self.typ == 'hor' and self.blocks[0].cur_rect.left <= self.init_point.x \
                or self.blocks[1].cur_rect.right >= self.init_point.x + self.dist:
            self.movement.x *= -1
        elif self.typ == 'vert' and self.blocks[0].cur_rect.top <= self.init_point.y \
                    or self.blocks[-1].cur_rect.bottom >= self.init_point.y + self.dist:
            self.movement.x *= -1


class Camera:

    def __init__(self, surf: pygame.Surface):
        self.surf = surf
        self.offset = pygame.math.Vector2(0, 0)
        self.display_size = pygame.math.Vector2(DISP_WIDTH, DISP_HEIGHT)

    def scroll(self, player: Player) -> tuple:
        self.offset.x = min(max(0, player.cur_rect.centerx - self.display_size.x // 2),
                            self.surf.get_width() - self.display_size.x)
        self.offset.y = min(max(0, player.cur_rect.centery - self.display_size.y // 2),
                            self.surf.get_height() - self.display_size.y)
        return self.offset.x, self.offset.y, self.display_size.x, self.display_size.y
