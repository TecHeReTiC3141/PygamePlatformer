import pygame.math

from classes.entity import *


# TODO hardcode moving parameters
class Player(Entity):
    sprites: dict[str, pygame.Surface] \
        = {i: pygame.image.load(f'resources/images/entities/player/player_sprite_{i}.png').convert_alpha()
           for i in ['left', 'right']}
    size = (90, 110)

    jump_strength = 60
    max_jump_cooldown = 25
    max_shoot_cooldown = 20
    falling_momentum = 3
    friction = -.3
    max_vel = 5
    max_health = 12
    speed = 2
    in_water = False
    charged = False
    ready_to_shoot = ()

    def __init__(self, x, y, direction='left'):
        super().__init__(x, y, direction)

        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.falling_momentum)
        self.angle = 0

        self.jump_cooldown = 0
        self.shoot_cooldown = 0

        self.is_jump = False
        self.air_time = 0

        self.collided_sides = {i: False for i in directions}

        self.score = 0
        self.keys = 0

    def hor_move(self, dt, fly: bool):
        if self.in_water:
            return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.acceleration.x -= .3
            self.direction = 'left'
            # if 3 * pi / 2 <= self.angle or self.angle <= pi / 2:
            #     self.angle = pi - self.angle

        if keys[pygame.K_d]:
            self.acceleration.x += .3
            self.direction = 'right'
        #
        if fly and keys[pygame.K_w]:
            self.rect.y -= 25
            if pi / 2 <= self.angle <= 3 * pi / 2:
                self.angle = (3 * pi - self.angle) % 360

        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.cap_hor_speed()
        self.rect.x += round(self.velocity.x * dt + .5 * self.acceleration.x * dt ** 2)

        self.angle %= pi * 2

    def vert_move(self, dt):
        self.velocity.y += self.acceleration.y * dt
        self.velocity.y = min(self.velocity.y, 12)
        self.rect.y += int(self.velocity.y * dt + .5 * self.acceleration.y * dt ** 2)

    def cap_hor_speed(self):
        if abs(self.velocity.x) < .01:
            self.velocity.x = 0
        self.velocity.x = max(-self.max_vel, min(self.velocity.x, self.max_vel))

    def get_angle(self, offset: pygame.math.Vector2, camera_size: pygame.math.Vector2, res: tuple):
        m_x, m_y = pygame.mouse.get_pos()
        m_x = round(m_x * camera_size.x / res[0] + offset.x)
        m_y = round(m_y * camera_size.y / res[1] + offset.y)
        c_x, c_y = self.rect.center
        dist = sqrt((c_x - m_x) ** 2 + (c_y - m_y) ** 2)
        self.angle = acos((m_x - c_x) / max(dist, .01))
        if m_y >= c_y:
            self.angle = 2 * pi - self.angle

    def update(self, dt=1):
        # print(self.velocity, self.acceleration)
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
        else:
            self.air_time += 1

        self.velocity.x = 0
        if self.acceleration.x > 0:
            self.acceleration.x = max(self.acceleration.x - .22, 0)
        else:
            self.acceleration.x = min(self.acceleration.x + .22, 0)
        if self.collided_sides['up']:
            self.velocity.y = 0

        max_sliding_down = 30

        if self.collided_sides['down']:
            max_sliding_down = 0

        if self.collided_sides['left']:
            max_sliding_down = .6
            if not self.collided_sides['down']:
                self.acceleration.x = max(0, self.acceleration.x)

        if self.collided_sides['right']:
            max_sliding_down = .6
            if not self.collided_sides['down']:
                self.acceleration.x = min(0, self.acceleration.x)

        self.velocity.y = min(self.velocity.y + min(self.acceleration.y * dt,
                                                    max_sliding_down), max_sliding_down)
        # print(self.collided_sides)
        for direct in self.collided_sides:
            self.collided_sides[direct] = False

        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.hit_cooldown > 0:
            self.hit_cooldown -= 1
        self.charged = False

    def jump(self):
        if self.jump_cooldown <= 0 and not self.is_jump and self.air_time <= 6:
            self.jump_cooldown = self.max_jump_cooldown
            self.velocity.y = -self.jump_strength
            self.is_jump = True

    def shoot(self,  offset: pygame.math.Vector2,
             camera_size: pygame.math.Vector2, res: tuple, proj_type: type) -> Projectile:
        self.shoot_cooldown = self.max_shoot_cooldown
        if not self.ready_to_shoot:

            self.ready_to_shoot = ()
            return proj_type(self.rect.centerx, self.rect.centery,
                             pygame.math.Vector2(cos(self.angle), -sin(self.angle)), self)

        m_x, m_y = pygame.mouse.get_pos()
        m_x = round(m_x * camera_size.x / res[0] + offset.x)
        m_y = round(m_y * camera_size.y / res[1] + offset.y)
        or_x, or_y = self.ready_to_shoot[0]
        d_x, d_y = or_x - m_x, or_y - m_y
        dist = sqrt(d_x ** 2 + d_y ** 2)
        angle = acos(d_x / max(dist, .01))
        if d_y > 0:
            angle = 2 * pi - angle
        movement_vector = pygame.math.Vector2(cos(angle), -sin(angle))
        proj: Projectile = proj_type(self.rect.centerx, self.rect.centery, movement_vector, self)
        proj.velocity *= sqrt(dist) // 5
        self.ready_to_shoot = ()
        return proj

    def draw(self, surface: pygame.Surface, offset: pygame.math.Vector2,
             camera_size: pygame.math.Vector2, res: tuple):
        self.image.fill('yellow')
        self.image.blit(self.sprites[self.direction], (0, 0))

        eye_x = 23 if self.direction == 'left' else 30
        pygame.draw.rect(self.image, 'blue' if not self.charged else 'purple',
                         (eye_x + cos(self.angle) * 5, 27 - sin(self.angle) * 5, 5, 5))
        pygame.draw.rect(self.image, 'blue' if not self.charged else 'purple',
                         (eye_x + 30 + cos(self.angle) * 5, 27 - sin(self.angle) * 5, 5, 5))
        if self.shoot_cooldown:
            pygame.draw.rect(surface, 'black',
                             (self.rect.x - 5, self.rect.y - 30, self.rect.width + 10, 25))
            pygame.draw.rect(surface, 'blue',
                             (self.rect.x - 2, self.rect.y - 27,
                              round((self.rect.width + 6) *
                                    (self.max_shoot_cooldown - self.shoot_cooldown) / self.max_shoot_cooldown), 19))
        if self.hit_cooldown <= 0 or self.hit_cooldown % 4 > 1:
            surface.blit(self.image, self.rect)

        if self.ready_to_shoot:
            m_x, m_y = pygame.mouse.get_pos()
            m_x = round(m_x * camera_size.x / res[0] + offset.x)
            m_y = round(m_y * camera_size.y / res[1] + offset.y)
            or_x, or_y = self.ready_to_shoot[0]
            d_x, d_y = or_x - m_x, or_y - m_y
            dist = sqrt(d_x ** 2 + d_y ** 2)
            angle = acos(d_x / max(dist, .01))
            if d_y > 0:
                angle = 2 * pi - angle
            pygame.draw.line(surface, 'purple', self.ready_to_shoot[0], (m_x, m_y), width=5)

            # sketching of projectile trajectory
            point = pygame.math.Vector2(self.rect.center)
            proj = self.ready_to_shoot[1](0, 0, pygame.math.Vector2(0.1, .1), self)
            movement_vector = pygame.math.Vector2(cos(angle), -sin(angle))
            vel = pygame.math.Vector2(proj.speed * sqrt(dist) // 6 * movement_vector)
            acc = pygame.math.Vector2(0, proj.falling_momentum)
            for pos in range(6, 0, -1):
                point += vel * int(sqrt(dist)) // 2
                vel += acc * int(sqrt(dist)) // 2
                pygame.draw.circle(surface, 'black', (point[0], point[1]), pos)




class PlayerOnMap(Player):
    speed = 8
    sprites: dict[str, pygame.Surface] \
        = {i: pygame.image.load(f'resources/images/entities/player/player_eyes_{i}.png').convert_alpha()
           for i in directions}

    def __init__(self, x, y):
        super().__init__(x, y)
        self.target: tuple = self.rect.center

    def set_position(self, pos: tuple):
        self.target = pos
        hyp = sqrt((pos[0] - self.rect.centerx) ** 2 + (pos[1] - self.rect.centery) ** 2)
        self.velocity = pygame.math.Vector2(((pos[0] - self.rect.centerx) / hyp),
                                            ((pos[1] - self.rect.centery) / hyp))
        if abs(self.velocity.x) > abs(self.velocity.y):
            self.direction = 'left' if self.velocity.x < 0 else 'right'
        else:
            self.direction = 'up' if self.velocity.y < 0 else 'down'

    def move(self, dt):
        self.rect.move_ip(self.velocity * self.speed)
        if self.rect.collidepoint(self.target):
            self.target = self.rect.center
            self.velocity *= 0

    def update(self, dt=1):
        self.move(dt)

    def draw(self, surface: pygame.Surface, res: tuple=()):
        self.image.fill('yellow')
        self.image.blit(self.sprites[self.direction], (0, 0))
        surface.blit(self.image, self.rect)
