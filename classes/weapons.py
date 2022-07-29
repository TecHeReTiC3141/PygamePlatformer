import pygame
from math import *
from random import *

# TODO Implement pixel-perfect collisions for projectiles
class Projectile:
    size = (40, 40)
    speed = 12
    damage = 1
    sprite = pygame.Surface(size)

    def __init__(self, x, y, movement_vector: pygame.math.Vector2, owner):
        self.angle = acos(movement_vector.x)
        if movement_vector.y > 0:
            self.angle = 2 * pi - self.angle

        self.owner = owner
        self.surf = pygame.Surface(self.size)
        self.surf.set_colorkey('black')
        self.mask = pygame.mask.from_surface(self.surf)

        self.rect = self.surf.get_rect(topleft=(x, y))
        self.vector = movement_vector
        self.alive = True
        pygame.draw.circle(self.surf, 'blue',
                           (self.rect.width // 2, self.rect.height // 2), self.rect.width // 4)

        pygame.draw.circle(self.surf, 'lightblue',
                       (self.rect.width // 2, self.rect.height // 2), self.rect.width // 2, 5)
    def move(self):
        self.rect.move_ip(self.vector * self.speed)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.surf, self.rect)

    def update(self):
        self.move()

    def set_angle(self, alpha):
        self.angle = (self.angle + alpha) % (2 * pi)
        self.vector = pygame.math.Vector2(cos(self.angle), -sin(self.angle))
        self.sprite = pygame.transform.rotate(self.sprite, degrees(alpha))

        self.size = self.sprite.get_size()
        self.surf = pygame.Surface(self.size)
        self.surf.set_colorkey('black')
        self.mask = pygame.mask.from_surface(self.surf)
        self.surf.blit(self.sprite, (0, 0))
        self.rect = self.surf.get_rect(topleft=self.rect.topleft)

    def interact(self, entity) -> bool:
        if self.rect.colliderect(entity.rect) and entity != self.owner:
            # if self.mask.overlap(entity.mask,
            #                      (entity.rect.left - self.rect.left, entity.rect.top - self.rect.top)):
            self.alive = False
            if isinstance(entity, Projectile):
                if randint(0, 2):
                    entity.alive = False
                else:
                    entity.set_angle(uniform(-pi / 2, pi / 2))
            return True
        return False


class Rocket(Projectile):
    damage = 1
    speed = 10
    sprite = pygame.transform.rotate(
        pygame.image.load('resources/images/entities/projectiles/small_rocket.png').convert_alpha(),
        270
    )

    def __init__(self, x, y, movement_vector: pygame.math.Vector2, owner):
        self.angle = acos(movement_vector.x)
        if movement_vector.y > 0:
            self.angle = 2 * pi - self.angle
        self.sprite = pygame.transform.rotate(self.sprite, degrees(self.angle))
        self.size = self.sprite.get_size()

        super().__init__(x, y, movement_vector, owner)
        self.surf.fill('black')
        self.surf.blit(self.sprite, (0, 0))

    def interact(self, entity) -> bool:
        if self.rect.colliderect(entity.rect) and entity != self.owner:
            if isinstance(entity, Projectile):
                entity.alive = False
            else:
                self.alive = False
            return True
        return False
