import pygame.sprite

from scripts.const import *
from classes.weapons import *


class Player:
    sprites: dict[str, pygame.Surface] \
        = {i: pygame.image.load(f'resources/images/entities/player/player_sprite_{i}.png').convert_alpha()
           for i in ['left', 'right']}
    size = (90, 110)

    jump_strength = 5
    max_jump_cooldown = 30
    falling_momentum = 0.25

    def __init__(self, x, y):
        self.image = pygame.Surface(self.size)
        self.image.set_colorkey('yellow')
        self.rect = self.image.get_rect(topleft=(x, y))
        self.prev_rect = self.rect.copy()
        self.movement = pygame.math.Vector2(0, 0)
        self.angle = 0
        self.direction = 'left'
        self.speed = 5
        self.jump_cooldown = 0
        self.is_jump = False
        self.air_time = 0

        self.collided_sides = {i: False for i in directions}

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.movement.x -= 1
            if 3 * pi / 2 <= self.angle or self.angle <= pi / 2:
                self.angle = pi - self.angle
        if keys[pygame.K_d]:
            self.movement.x += 1
            if pi / 2 <= self.angle <= 3 * pi / 2:
                self.angle = (3 * pi - self.angle) % 360

        self.angle %= pi * 2

    def get_angle(self, offset: pygame.math.Vector2):
        m_x, m_y = pygame.mouse.get_pos()
        m_x += offset.x
        m_y += offset.y
        c_x, c_y = self.rect.center
        dist = sqrt((c_x - m_x) ** 2 + (c_y - m_y) ** 2)
        self.angle = acos((m_x - c_x) / dist)
        if m_y >= c_y:
            self.angle = 2 * pi - self.angle

    def update(self, dt):

        self.prev_rect = self.rect.copy()
        # if self.movement.length():
        #     norm_move = self.movement.normalize()
        if self.movement.x > 0 or pi / 2 >= self.angle or self.angle >= 3 * pi / 2:
            self.direction = 'right'
        elif self.movement.x < 0 or pi / 2 <= self.angle <= 3 * pi / 2:
            self.direction = 'left'

        if any([self.collided_sides['down'],
                self.collided_sides['left'], self.collided_sides['right']]):
            self.is_jump = False
            self.air_time = 0

        if self.is_jump:
            self.air_time += 1

        self.movement.x = 0
        if self.collided_sides['up']:
            self.movement.y = 0

        max_sliding_down = 3
        if self.collided_sides['down']:
            max_sliding_down = 0


        elif self.collided_sides['left'] or self.collided_sides['right']:
            max_sliding_down = .4
        self.movement.y = min(self.movement.y + self.falling_momentum * dt, max_sliding_down)

        for direct in self.collided_sides:
            self.collided_sides[direct] = False

        self.jump_cooldown -= 1

    def jump(self, dt):
        if self.jump_cooldown <= 0 and not self.is_jump and self.air_time <= 6:
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

    def shoot(self) -> Projectile:
        return Projectile(self.rect.centerx, self.rect.centery,
                          pygame.math.Vector2(cos(self.angle), -sin(self.angle)))

    def draw(self, surface: pygame.Surface):
        self.image.fill('yellow')
        self.image.blit(self.sprites[self.direction], (0, 0))

        eye_x = 23 if self.direction == 'left' else 30
        pygame.draw.rect(self.image, 'blue',
                         (eye_x + cos(self.angle) * 5, 27 - sin(self.angle) * 5, 5, 5))
        pygame.draw.rect(self.image, 'blue',
                         (eye_x + 30 + cos(self.angle) * 5, 27 - sin(self.angle) * 5, 5, 5))

        if self.collided_sides['down']:
            pygame.draw.line(self.image, 'red', (0, self.rect.height - 5),
                             (self.rect.right, self.rect.height - 5), 5)
        if self.collided_sides['left']:
            pygame.draw.line(self.image, 'red', (0, 0),
                             (0, self.rect.height), 5)
        if self.collided_sides['right']:
            pygame.draw.line(self.image, 'red', (self.rect.width, 0),
                             (self.rect.width, self.rect.height), 5)
        surface.blit(self.image, self.rect)
