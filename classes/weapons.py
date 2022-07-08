import pygame

class Projectile:

    size = (25, 25)
    speed = 10
    damage = 1

    def __init__(self, x, y, movement_vector: pygame.math.Vector2, owner):
        self.owner = owner
        self.surf = pygame.Surface(self.size)
        self.surf.set_colorkey('black')
        self.rect = self.surf.get_rect(topleft=(x, y))
        self.vector = movement_vector
        self.alive = True
        pygame.draw.circle(self.surf, 'blue',
                           (self.rect.width // 2, self.rect.height // 2), self.rect.width // 2)

    def move(self):
        self.rect.move_ip(self.vector * self.speed)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.surf, self.rect)

    def update(self):

        self.move()

    def interact(self, entity) -> bool:
        if self.rect.colliderect(entity.rect) and entity != self.owner:
            self.alive = False
            return True
        return False


class Rocket(Projectile):
    damage = 2
    sprites = {
        'up': pygame.image.load('resources/images/entities/projectiles/small_rocket.png').convert_alpha(),
        'left': pygame.transform.rotate(
            pygame.image.load('resources/images/entities/projectiles/small_rocket.png').convert_alpha(),
            90
        ),
        'down': pygame.transform.rotate(
            pygame.image.load('resources/images/entities/projectiles/small_rocket.png').convert_alpha(),
            180
        ),
        'right': pygame.transform.rotate(
            pygame.image.load('resources/images/entities/projectiles/small_rocket.png').convert_alpha(),
            270
        )
    }

    def __init__(self, x, y, dir, movement_vector: pygame.math.Vector2, owner):
        if dir in ['up', 'down']:
            self.size = self.sprites['up'].get_size()
        else:
            self.size = self.sprites['left'].get_size()

        super().__init__(x, y, movement_vector, owner)
        self.surf.fill('black')
        self.surf.blit(self.sprites[dir], (0, 0))





