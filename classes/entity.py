import pygame

from scripts.const import *
from classes.weapons import *

class Entity:

    sprites: dict[str, pygame.Surface] = []
    size: tuple = (BLOCK_SIZE, BLOCK_SIZE)
    max_health = 30

    def __init__(self, x, y, width, height):
        x, y, width, height = x * SCALE, y * SCALE, width * SCALE, height * SCALE
        self.image = pygame.Surface(self.size)
        self.image.set_colorkey('yellow')
        self.rect = self.image.get_rect(topleft=(x, y))
        self.prev_rect = self.rect.copy()
        self.health = self.max_health
        self.direction = ""
        self.alive = True

    def update(self):
        pass

    def draw(self, surface: pygame.Surface):
        self.image.fill('yellow')
        self.image.blit(self.sprites[self.direction], (0, 0))

        surface.blit(self.image, self.rect)

    def die(self):
        self.alive = False


class Cannon(Entity):

    proj_speed = 5
    max_shoot_cooldown = 30

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

    def __init__(self, x, y, width, height, dir):
        if dir in ['up', 'down']:
            self.size = (60, 76)
            self.velocity = pygame.math.Vector2(0, self.proj_speed if dir == 'down' else -self.proj_speed)
        else:
            self.size = (76, 60)
            self.velocity = pygame.math.Vector2(self.proj_speed if dir == 'right' else -self.proj_speed, 0)
        super().__init__(x, y, width, height)
        self.shoot_cooldown = self.max_shoot_cooldown

    def shoot(self) -> Projectile:
        return Rocket(self.rect.x, self.rect.y, self.direction, self.velocity)

    def update(self):
        self.shoot_cooldown -= 1
        if self.shoot_cooldown <= 0:
            self.shoot_cooldown = self.max_shoot_cooldown
            return self.shoot()
