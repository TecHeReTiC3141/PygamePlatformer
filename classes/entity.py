from scripts.const import *
from classes.weapons import *


class Entity:
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

        self.image.fill('yellow')
        self.image.blit(pygame.transform.scale(self.sprites[self.direction], self.size), (0, 0))
        self.hit_cooldown = 0
        self.alive = True

    def update(self, dt=1):
        if self.has_hit_cooldown:
            self.hit_cooldown -= 1

    def draw(self, surface: pygame.Surface):
        if self.hit_cooldown <= 0 or self.hit_cooldown % 4 > 1:
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
    max_shoot_cooldown = 40
    has_hit_cooldown = False
    sprites = {
        'up': pygame.image.load('resources/images/entities/cannon/green_cannon.png').convert_alpha(),
        'left': pygame.transform.rotate(
            pygame.image.load('resources/images/entities/cannon/green_cannon.png').convert_alpha(),
            90
        ),
        'down': pygame.transform.rotate(
            pygame.image.load('resources/images/entities/cannon/green_cannon.png').convert_alpha(),
            180
        ),
        'right': pygame.transform.rotate(
            pygame.image.load('resources/images/entities/cannon/green_cannon.png').convert_alpha(),
            270
        )
    }

    def __init__(self, x, y, width, height, direction):
        if direction in ['up', 'down']:
            self.size = (width * SCALE, height * SCALE)
            self.velocity = pygame.math.Vector2(0, self.proj_speed if direction == 'down' else -self.proj_speed)
        else:
            self.size = (height * SCALE, width * SCALE)
            self.velocity = pygame.math.Vector2(self.proj_speed if direction == 'right' else -self.proj_speed, 0)
        super().__init__(x, y, direction)
        self.shoot_cooldown = self.max_shoot_cooldown
        print(x, y, self.rect)

    def shoot(self) -> Projectile:
        return Rocket(self.rect.x, self.rect.y, self.direction, self.velocity, self)

    def update(self, dt=1):
        self.shoot_cooldown -= 1
        if self.shoot_cooldown <= 0:
            self.shoot_cooldown = self.max_shoot_cooldown
            return self.shoot()

    def draw(self, surface: pygame.Surface):
        super().draw(surface)
        pygame.draw.rect(surface, 'red', self.rect, width=5)
