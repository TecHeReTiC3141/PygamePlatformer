from classes.player import *


class Block:
    movable = False

    def __init__(self, x, y, surface: pygame.Surface):
        self.surface = pygame.transform.scale(surface, (BLOCK_SIZE, BLOCK_SIZE))

        self.rect = self.surface.get_rect(topleft=(x * BLOCK_SIZE, y * BLOCK_SIZE))
        self.left_outer_rect = pygame.Rect(self.rect.left - 3, self.rect.top,
                                           3, self.rect.height)
        self.right_outer_rect = pygame.Rect(self.rect.right, self.rect.top,
                                            3, self.rect.height)
        self.up_outer_rect = pygame.Rect(self.rect.left, self.rect.top - 3,
                                         self.rect.width, 3)

    def collide(self, entity: Player, mode: str) -> str:

        if entity.rect.colliderect(self.rect):
            if mode == 'v':
                # left side
                if entity.velocity.x > 0:
                    entity.rect.right = self.rect.left
                    entity.collided_sides['right'] = True
                    return 'right'

                # right side
                elif entity.velocity.x < 0:
                    entity.rect.left = self.rect.right
                    entity.collided_sides['left'] = True
                    return 'left'

            elif mode == 'h':
                # top side
                if entity.velocity.y > 0:
                    entity.rect.bottom = self.rect.top
                    entity.collided_sides['down'] = True
                    return 'down'

                # bottom side
                elif entity.velocity.y < 0:
                    entity.rect.top = self.rect.bottom
                    entity.collided_sides['top'] = True
                    return 'top'

        elif mode == 'h' and entity.rect.colliderect(self.up_outer_rect):
            entity.collided_sides['down'] = True
            return 'down'

        elif mode == 'v' and entity.rect.colliderect(self.left_outer_rect):
            entity.collided_sides['right'] = True
            return 'right'

        elif mode == 'v' and entity.rect.colliderect(self.right_outer_rect):
            entity.collided_sides['left'] = True
            return 'left'

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


class GameObject:
    sprites: dict[int, pygame.Surface] = {}
    alive = True

    def __init__(self, x, y, width, height, surface: pygame.Surface):
        x, y, width, height = x * SCALE, y * SCALE, width * SCALE, height * SCALE
        self.surface = pygame.transform.scale(surface, (width, height)).convert_alpha()
        self.rect = self.surface.get_rect(topleft=(x, y))

    def draw(self, surface: pygame.Surface):
        surface.blit(self.surface, self.rect)

    def interact(self, *args):
        pass

    def update(self):
        pass


class Decor(GameObject):
    pass


class Obstacle(GameObject, Block):
    pass


class Collectable(GameObject):
    pass


class Animated(GameObject):
    frames_per_sprite = 4

    def __init__(self, x, y, width, height, surface: pygame.Surface):
        super().__init__(x, y, width, height, surface)
        self.frame_count = 0

    def draw(self, surface: pygame.Surface):
        surface.blit(self.sprites[self.frame_count // self.frames_per_sprite], self.rect)
        self.frame_count += 1
        self.frame_count %= self.frames_per_sprite * len(self.sprites)


# TODO add sprite
class MovingPlatform(Block, GameObject):

    def __init__(self, x, y, width, height, surface: pygame.Surface, typ: str, dist, speed=5):
        self.init_point = pygame.math.Vector2(x * SCALE, y * SCALE)

        GameObject.__init__(self, x, y, width, height, surface)
        self.left_outer_rect = pygame.Rect(self.rect.left - 3, self.rect.top,
                                           3, self.rect.height)
        self.right_outer_rect = pygame.Rect(self.rect.right, self.rect.top,
                                            3, self.rect.height)
        self.up_outer_rect = pygame.Rect(self.rect.left, self.rect.top - 3,
                                         self.rect.width, 3)

        self.dist = dist * BLOCK_SIZE
        self.typ = typ
        self.movement = pygame.math.Vector2(0 if typ == 'vert' else speed,
                                            0 if typ == 'hor' else speed)

    def move(self):
        self.rect.move_ip(self.movement)
        self.left_outer_rect.move_ip(self.movement)
        self.right_outer_rect.move_ip(self.movement)
        self.up_outer_rect.move_ip(self.movement)
        if self.typ == 'hor' and (self.rect.left < self.init_point.x
                                  or self.rect.left > self.init_point.x + self.dist):
            self.movement *= -1
        elif self.typ == 'vert' and (self.rect.top < self.init_point.y
                                     or self.rect.top > self.init_point.y + self.dist):
            self.movement *= -1

    def interact(self, player: Player):
        side = self.collide(player, 'h') or self.collide(player, 'v')
        if side:
            print(player.velocity, player.collided_sides)

            player.rect.move_ip(self.movement)

    def update(self):
        self.move()

    def collide(self, entity: Player, mode: str) -> str:
        if entity.rect.colliderect(self.rect):
            if mode == 'v':
                # left side
                if entity.prev_rect.right <= self.rect.left <= entity.rect.right:
                    entity.rect.right = self.rect.left
                    entity.collided_sides['right'] = True
                    return 'right'

                # right side
                if entity.prev_rect.left >= self.rect.right >= entity.rect.left:
                    entity.rect.left = self.rect.right
                    entity.collided_sides['left'] = True
                    return 'left'

            elif mode == 'h':
                # top side
                if entity.prev_rect.bottom <= self.rect.top <= entity.rect.bottom:
                    entity.rect.bottom = self.rect.top
                    entity.collided_sides['down'] = True
                    return 'down'

        elif mode == 'h' and entity.rect.colliderect(self.up_outer_rect):
            entity.collided_sides['down'] = True
            return 'down'

        elif mode == 'v' and entity.rect.colliderect(self.left_outer_rect):
            entity.collided_sides['right'] = True
            return 'right'

        elif mode == 'v' and entity.rect.colliderect(self.right_outer_rect):
            entity.collided_sides['left'] = True
            return 'left'


class LevelEnd(GameObject):
    sprites = {0: 'resources/images/surrounding/door_closed.png',
               1: 'resources/images/surrounding/door_open.png'}

    def __init__(self, x, y, width, height, surface: pygame.Surface):
        super().__init__(x, y, width, height, surface)
        self.active_zone = pygame.Rect(self.rect.x - self.rect.width,
                                       self.rect.y,
                                       self.rect.width * 3, self.rect.height)
        self.active = 0

    def interact(self, player: Player):

        if player.rect.colliderect(self.active_zone):
            print('active')
            if not self.active:
                self.surface = pygame.image.load(self.sprites[1]).convert_alpha()
                self.surface = pygame.transform.scale(self.surface, (self.surface.get_width() * SCALE,
                                                                     self.surface.get_height() * SCALE))
            self.active = 1

        elif self.active:
            self.active = 0
            self.surface = pygame.image.load(self.sprites[0]).convert_alpha()
            self.surface = pygame.transform.scale(self.surface, (self.surface.get_width() * SCALE,
                                                                 self.surface.get_height() * SCALE))


class Coin(Animated, Collectable):
    sprite_size = (70, 69)
    sprites: dict[int, pygame.Surface] = {
        i: pygame.transform.scale(
            pygame.image.load(f'resources/images/surrounding/coins/gold_coin_{i}.png').convert_alpha(),
            (70, 69))
        for i in range(7)}

    value = 50

    def __init__(self, x, y, width, height, surface: pygame.Surface):
        super().__init__(x, y, width, height, surface)
        self.frame_count = 0

    def interact(self, player: Player):
        if player.rect.colliderect(self.rect):
            player.score += self.value
            self.value = 0
            self.alive = False

# TODO implement keys which player must collect to open LevelEnd.
