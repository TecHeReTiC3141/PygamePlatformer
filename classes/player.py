from scripts.const import *


class Player:

    sprites: dict[str, pygame.Surface] \
        = {i: pygame.image.load(f'resources/images/entities/heretic/heretic_sprite_{i}.png')
               for i in directions}
    size = (75, 100)

    jump_strength = 8
    max_jump_cooldown = 30

    def __init__(self, x, y, ):
        self.surface = pygame.Surface(self.size)
        self.cur_rect = self.surface.get_rect(topleft=(x, y))
        self.prev_rect = self.cur_rect.copy()
        self.movement = pygame.math.Vector2(0, 0)
        self.angle = 0
        self.direction = 'left'
        self.speed = 5
        self.jump_cooldown = 0
        self.is_jump = False

        self.collided_sides = {i: False for i in directions}

    def move(self):
        # if self.jump_cooldown >= self.max_jump_cooldown // 2:
        #     return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.movement.x -= 1
            if 3 * pi / 2 <= self.angle or self.angle <= pi / 2:
                self.angle = pi - self.angle
        if keys[pygame.K_d]:
            self.movement.x += 1
            if pi / 2 <= self.angle <= 3 * pi / 2:
                self.angle = (3 * pi - self.angle) % 360

        if keys[pygame.K_UP]:
            self.angle += 0.03
        if keys[pygame.K_DOWN]:
            self.angle -= 0.03

        self.angle %= pi * 2

    def update(self):

        self.prev_rect = self.cur_rect.copy()
        self.move()
        # if self.movement.length():
        #     norm_move = self.movement.normalize()
        self.cur_rect.move_ip(self.movement * self.speed)
        if self.movement.x > 0:
            self.direction = 'right'
        elif self.movement.x < 0:
            self.direction = 'left'

        if any([self.collided_sides['down'],
                self.collided_sides['left'], self.collided_sides['right']]):
            self.is_jump = False

        self.movement.x = 0
        sliding_down = 1.5
        if self.collided_sides['down']:
            sliding_down = 0

        elif self.collided_sides['left'] or self.collided_sides['right']:
            sliding_down = .4
        self.movement.y = min(self.movement.y + sliding_down, sliding_down)

        for direct in self.collided_sides:
            self.collided_sides[direct] = False

        self.jump_cooldown -= 1


    def jump(self):
        if self.jump_cooldown <= 0:
            self.jump_cooldown = self.max_jump_cooldown
            if self.collided_sides['left']:
                self.movement.y = -self.jump_strength // 2
                self.movement.x = -self.jump_strength
            elif self.collided_sides['right']:
                self.movement.y = -self.jump_strength // 2
                self.movement.x = -self.jump_strength
            else:
                self.movement.y = -self.jump_strength
            self.is_jump = True


    def draw(self, surface: pygame.Surface):

        self.surface.blit(self.sprites[self.direction], (0, 0))
        pygame.draw.rect(self.surface, 'red',
                         (20 + cos(self.angle) * 5, 20 - sin(self.angle) * 5, 5, 5))
        pygame.draw.rect(self.surface, 'red',
                         (40 + cos(self.angle) * 5, 20 - sin(self.angle) * 5, 5, 5))
        if self.collided_sides['down']:
            pygame.draw.line(self.surface, 'red', (0, self.cur_rect.height - 5),
                             (self.cur_rect.right, self.cur_rect.height - 5), 5)
        if self.collided_sides['left']:
            pygame.draw.line(self.surface, 'red', (0, 0),
                             (0, self.cur_rect.height), 5)
        if self.collided_sides['right']:
            pygame.draw.line(self.surface, 'red', (self.cur_rect.width, 0),
                             (self.cur_rect.width, self.cur_rect.height), 5)
        surface.blit(self.surface, self.cur_rect)
