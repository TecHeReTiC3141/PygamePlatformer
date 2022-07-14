from scripts.const import *
from classes.weapons import *


class Entity:
    sprite: pygame.Surface = None
    sprites: dict[str, pygame.Surface] = {}
    size: tuple = (BLOCK_SIZE, BLOCK_SIZE)
    max_health = 30
    max_hit_cooldown = 90
    has_hit_cooldown = True

    def __init__(self, x, y, direction):
        x, y = x * SCALE, y * SCALE
        self.image = pygame.Surface(self.size)
        self.image.set_colorkey('yellow')
        self.rect = self.image.get_rect(topleft=(x, y))
        self.prev_rect = self.rect.copy()
        self.health = self.max_health
        self.direction = direction
        self.target = None

        self.image.fill('yellow')

        self.hit_cooldown = 0
        self.alive = True

    def update(self, dt=1):
        if self.has_hit_cooldown:
            self.hit_cooldown -= 1

    def draw(self, surface: pygame.Surface):
        if not self.has_hit_cooldown or self.hit_cooldown <= 0 or self.hit_cooldown % 4 > 1:
            surface.blit(self.image, self.rect)

    def hurt(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()
        if self.has_hit_cooldown:
            self.hit_cooldown = self.max_hit_cooldown

    def die(self):
        self.alive = False


class Cannon(Entity):
    max_health = 5
    proj_speed = 3
    max_shoot_cooldown = 60
    has_hit_cooldown = False
    is_on = False
    max_dist = 1000
    sprite = pygame.transform.rotate(
            pygame.image.load('resources/images/entities/cannon/green_cannon.png').convert_alpha(),
            270)

    def __init__(self, x, y, width, height, direction, target: Entity, fixed=False):
        if direction in ['up', 'down']:
            self.size = (width * SCALE, height * SCALE)
            self.velocity = pygame.math.Vector2(0, 1 if direction == 'down' else -1)
            self.angle = pi / 2 if direction == 'up' else 3 * pi / 2
        else:
            self.size = (height * SCALE, width * SCALE)
            self.velocity = pygame.math.Vector2(1 if direction == 'right' else -1, 0)
            self.angle = 0 if direction == 'right' else pi

        super().__init__(x, y, direction)
        if direction in ['up', 'down']:
            self.base = self.rect.midbottom if self.direction == 'up' else self.rect.midtop
        else:
            self.base = self.rect.midright if self.direction == 'left' else self.rect.midleft

        self.image = pygame.transform.rotate(self.sprite, degrees(self.angle))

        self.rect = self.image.get_rect(topleft=(x * SCALE, y * SCALE))
        self.shoot_cooldown = self.max_shoot_cooldown
        self.fixed = fixed
        self.target = target
        print(x, y, self.rect)

    def shoot(self) -> Projectile:
        return Rocket(self.rect.centerx + cos(self.angle) * 5, self.rect.centery - sin(self.angle) * 5,
                   self.direction, self.velocity, self)

    def get_angle(self):
        t_x, t_y = self.target.rect.center
        b_x, b_y = self.base
        dist = sqrt((t_x - b_x) ** 2 + (t_y - b_y) ** 2)
        if not any([self.direction == 'left' and t_x < b_x,
                    self.direction == 'right' and t_x > b_x,
                    self.direction == 'up' and t_y < b_y,
                    self.direction == 'down' and t_y > b_y,
                    ]) or dist > self.max_dist:
            self.is_on = False
            return

        self.is_on = True

        angle = acos((t_x - b_x) / max(dist, .01))
        self.angle = angle if t_y <= b_y else 2 * pi - angle
        self.velocity = pygame.math.Vector2(cos(self.angle), -sin(self.angle))
        self.image =pygame.transform.rotate(self.sprite, degrees(self.angle))

        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, dt=1):
        if not self.fixed:
            self.get_angle()

        self.shoot_cooldown -= 1
        if self.shoot_cooldown <= 0 and self.is_on:
            self.shoot_cooldown = self.max_shoot_cooldown
            return self.shoot()

    def draw(self, surface: pygame.Surface):

        super().draw(surface)
        pygame.draw.rect(surface, 'red', self.rect, width=5)
