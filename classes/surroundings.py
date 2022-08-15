from pathlib import Path
from classes.player import *
from classes.decor import *


# TODO think about block's friction
class Block:
    movable = False

    def __init__(self, x, y, surface: pygame.Surface):
        self.surface = pygame.transform.scale(surface, (BLOCK_SIZE, BLOCK_SIZE))
        self.mask = pygame.mask.from_surface(self.surface)

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


class BackgroundBlock(Block):

    def __init__(self, x, y, surface: pygame.Surface):
        self.surface = pygame.transform.scale(surface, (BLOCK_SIZE, BLOCK_SIZE))
        self.mask = pygame.mask.from_surface(self.surface)

        self.rect = self.surface.get_rect(topleft=(x * BLOCK_SIZE, y * BLOCK_SIZE))

    def collide(self, entity: Player, mode: str) -> str:
        pass


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
    returns_decor = False

    def __init__(self, x, y, width, height, surface: pygame.Surface):
        x, y, width, height = x * SCALE, y * SCALE, width * SCALE, height * SCALE
        self.surface = pygame.transform.scale(surface, (width, height)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.surface)

        self.surface.set_colorkey('yellow')
        self.rect = self.surface.get_rect(topleft=(x, y))

    def draw(self, surface: pygame.Surface):
        surface.blit(self.surface, self.rect)

    def interact(self, *args):
        pass

    def update(self):
        pass


class Obstacle(GameObject, Block):
    def collide(self, entity: Player, mode: str) -> str:
        pass


class Collectable(GameObject):
    pass


class Moving(GameObject):
    padding = 40
    speed = 2

    def __init__(self, x, y, width, height, surface: pygame.Surface):
        super().__init__(x, y, width, height, surface)
        self.init_point = self.rect.center

    def draw(self, surface: pygame.Surface):
        super().draw(surface)
        self.move()

    def move(self):
        self.rect.y += self.speed
        if self.rect.y > self.init_point[1] + self.padding \
                or self.rect.y < self.init_point[1] - self.padding:
            self.speed *= -1


class Animated(GameObject):
    frames_per_sprite = 4

    def __init__(self, x, y, width, height, surface: pygame.Surface):
        super().__init__(x, y, width, height, surface)
        self.frame_count = 0

    def draw(self, surface: pygame.Surface):
        surface.blit(self.sprites[self.frame_count // self.frames_per_sprite], self.rect)
        self.frame_count += 1
        self.frame_count %= self.frames_per_sprite * len(self.sprites)


class MovingPlatform(Obstacle):

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

        if mode == 'h' and entity.rect.colliderect(self.up_outer_rect):
            entity.collided_sides['down'] = True
            return 'down'

        if mode == 'v' and entity.rect.colliderect(self.left_outer_rect):
            entity.collided_sides['right'] = True
            return 'right'

        if mode == 'v' and entity.rect.colliderect(self.right_outer_rect):
            entity.collided_sides['left'] = True
            return 'left'


class Water(Animated, Obstacle):
    source = Path('resources/images/surrounding/animated_water')
    sprites = {i: pygame.image.load(image).convert_alpha() for i, image in enumerate(source.glob('*.png'))}
    returns_decor = True

    def collide(self, entity: Player, mode: str) -> list[Decor]:
        if entity.rect.colliderect(self.rect) and not entity.in_water:
            entity.velocity *= 0
            entity.in_water = True
            particles = []
            for i in range(randint(7, 10)):
                x, y = randint(entity.rect.left, entity.rect.right), self.rect.top
                velocity = pygame.math.Vector2((x - entity.rect.centerx) // 8, randint(-30, -20))
                particles.append(WaterDrop(x, y, randint(8, 12), randint(8, 12), velocity,
                                           pygame.math.Vector2(0, falling_momentum),
                                           life_time=randint(80, 120)))
            return particles


class Spike(Obstacle):

    def __init__(self, x, y, width, height, surface: pygame.Surface):
        GameObject.__init__(self, x, y, width, height, surface)

    def collide(self, entity: Player, mode: str) -> str:
        if entity.rect.colliderect(self.rect) and entity.hit_cooldown <= 0:
            entity.hit_cooldown = entity.max_hit_cooldown
            if mode == 'v':
                # left side
                entity.hurt(1)
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
                    entity.health = 0
                    return 'down'

                # bottom side
                elif entity.velocity.y < 0:
                    entity.rect.top = self.rect.bottom
                    entity.collided_sides['top'] = True
                    entity.hurt(2)
                    return 'top'


class LevelEnd(GameObject):
    sprites = {0: 'resources/images/surrounding/door_closed.png',
               1: 'resources/images/surrounding/door_open.png'}

    def __init__(self, x, y, width, height, surface: pygame.Surface, key_count):
        super().__init__(x, y, width, height, surface)
        self.active_zone = pygame.Rect(self.rect.x - self.rect.width,
                                       self.rect.y,
                                       self.rect.width * 3, self.rect.height)
        self.active = 0
        self.key_count = key_count

    def interact(self, player: Player):

        if player.rect.colliderect(self.active_zone) and player.keys == self.key_count:
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
            self.alive = False


class Key(Moving, Collectable):

    def interact(self, player: Player):
        if player.rect.colliderect(self.rect):
            player.keys += 1
            self.alive = False
