import pygame

class Projectile:

    proj_size = (25, 25)
    speed = 10

    def __init__(self, x, y, movement_vector: pygame.math.Vector2):
        self.surf = pygame.Surface(self.proj_size)
        self.surf.set_colorkey('black')
        self.rect = self.surf.get_rect(topleft=(x, y))
        self.vector = movement_vector
        self.alive = True

    def move(self):
        self.rect.move_ip(self.vector * self.speed)

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(self.surf, 'blue',
                           (self.rect.width // 2, self.rect.height // 2), self.rect.width // 2)
        surface.blit(self.surf, self.rect)

    def update(self):

        self.move()

    def interact(self, entity):
        if self.rect.colliderect(entity.rect):
            self.alive = False

