import pygame.sprite

from scripts.const import *
from classes.weapons import *


class Player:
    sprites: dict[str, pygame.Surface] \
        = {i: pygame.image.load(f'resources/images/entities/player/player_sprite_{i}.png').convert_alpha()
           for i in ['left', 'right']}
    size = (90, 110)

    jump_strength = 55
    max_jump_cooldown = 30
    falling_momentum = 2.5
    friction = -.25
    max_vel = 5

    def __init__(self, x, y):
        self.image = pygame.Surface(self.size)
        self.image.set_colorkey('yellow')
        self.rect = self.image.get_rect(topleft=(x, y))
        self.prev_rect = self.rect.copy()
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.falling_momentum)
        self.angle = 0
        self.direction = 'left'
        self.speed = 2
        self.jump_cooldown = 0
        self.is_jump = False
        self.air_time = 0

        self.collided_sides = {i: False for i in directions}

    def hor_move(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.acceleration.x -= .25
            if 3 * pi / 2 <= self.angle or self.angle <= pi / 2:
                self.angle = pi - self.angle
        if keys[pygame.K_d]:
            self.acceleration.x += .25
            if pi / 2 <= self.angle <= 3 * pi / 2:
                self.angle = (3 * pi - self.angle) % 360

        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.cap_hor_speed()
        self.rect.x += int(self.velocity.x * dt + .5 * self.acceleration.x * dt ** 2)

        self.angle %= pi * 2

    def vert_move(self, dt):
        self.velocity.y += self.acceleration.y * dt
        self.velocity.y = min(self.velocity.y, 7)
        self.rect.y += int(self.velocity.y * dt + .5 * self.acceleration.y * dt ** 2)

    def cap_hor_speed(self):
        if abs(self.velocity.x) < .01:
            self.velocity.x = 0
        self.velocity.x = max(-self.max_vel, min(self.velocity.x, self.max_vel))

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
        # print(self.velocity, self.acceleration)
        self.prev_rect = self.rect.copy()
        # if self.movement.length():
        #     norm_move = self.movement.normalize()
        if self.velocity.x > 0 or pi / 2 >= self.angle or self.angle >= 3 * pi / 2:
            self.direction = 'right'
        elif self.velocity.x < 0 or pi / 2 <= self.angle <= 3 * pi / 2:
            self.direction = 'left'

        if any([self.collided_sides['down'],
                self.collided_sides['left'], self.collided_sides['right']]):
            self.is_jump = False
            self.air_time = 0

        if self.is_jump:
            self.air_time += 1

        self.velocity.x = 0
        if self.acceleration.x > 0:
            self.acceleration.x = max(self.acceleration.x - .15, 0)
        else:
            self.acceleration.x = min(self.acceleration.x + .15, 0)
        if self.collided_sides['up']:
            self.velocity.y = 0

        max_sliding_down = 5
        if self.collided_sides['down']:
            max_sliding_down = 0

        if self.collided_sides['left']:

            max_sliding_down = .4
            self.velocity.x = max(0, self.velocity.x)
            self.acceleration.x = max(0, self.acceleration.x)

        if self.collided_sides['right']:
            max_sliding_down = .4
            self.velocity.x = min(0, self.velocity.x)
            self.acceleration.x = min(0, self.acceleration.x)

        self.velocity.y = min(self.velocity.y + min(self.acceleration.y * dt,
                                                    max_sliding_down), max_sliding_down)
        # print(self.collided_sides)
        for direct in self.collided_sides:
            self.collided_sides[direct] = False

        self.jump_cooldown -= 1

    def jump(self):
        if self.jump_cooldown <= 0 and not self.is_jump and self.air_time <= 6:
            self.jump_cooldown = self.max_jump_cooldown
            if self.collided_sides['left']:
                self.velocity.y = -self.jump_strength // 2
                self.velocity.x = -self.jump_strength
            elif self.collided_sides['right']:
                self.velocity.y = -self.jump_strength // 2
                self.velocity.x = -self.jump_strength
            else:
                self.velocity.y = -self.jump_strength
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
