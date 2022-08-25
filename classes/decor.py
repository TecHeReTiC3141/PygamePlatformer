from scripts.const import *


class Decor:
    surface = pygame.Surface((10, 10))

    def __init__(self, x, y, life_time):
        self.rect = self.surface.get_rect(topleft=(x, y))
        self.life_time = life_time

    def draw(self, surface: pygame.Surface):
        surface.blit(self.surface, self.rect)

    def update(self):
        self.life_time -= 1


class Particle(Decor):
    has_physics = True

    def __init__(self, x, y, velocity: pygame.math.Vector2,
                 acceleration: pygame.math.Vector2, life_time):
        self.surface.set_colorkey('black')
        self.rect = self.surface.get_rect(center=(x, y))
        self.velocity = velocity
        self.acceleration = acceleration
        self.life_time = life_time
        self.max_life_time = life_time

    def update(self):
        if self.has_physics:
            self.rect.move_ip(self.velocity)
            self.velocity += self.acceleration
        super().update()


class WaterDrop(Particle):
    has_physics = True

    def __init__(self, x, y, width, height, velocity: pygame.math.Vector2,
                 acceleration: pygame.math.Vector2, life_time):
        self.surface = pygame.Surface((width, height))
        self.surface.fill('blue')
        super().__init__(x, y, velocity, acceleration, life_time)


class RocketSmoke(Particle):
    has_physics = False

    def __init__(self, x, y, radius, velocity: pygame.math.Vector2,
                 acceleration: pygame.math.Vector2, life_time):
        self.surface = pygame.Surface((radius * 2, radius * 2))
        super().__init__(x, y, velocity, acceleration, life_time)

    def draw(self, surface: pygame.Surface):
        self.surface.fill('black')
        pygame.draw.circle(self.surface, (round(255 * (self.max_life_time - self.life_time) / self.max_life_time),
                                          round(255 * (self.max_life_time - self.life_time) / self.max_life_time),
                                          round(255 * (self.max_life_time - self.life_time) / self.max_life_time)), (self.rect.width // 2, self.rect.height // 2),
                           round(self.rect.width // 2 * self.life_time / self.max_life_time))
        super().draw(surface)


class MagicFlashes(Particle):
    has_physics = False

    def __init__(self, x, y, radius, velocity: pygame.math.Vector2,
                 acceleration: pygame.math.Vector2, life_time):
        self.surface = pygame.Surface((radius * 2, radius * 2))
        super().__init__(x, y, velocity, acceleration, life_time)

    def draw(self, surface: pygame.Surface):
        self.surface.fill('black')
        pygame.draw.circle(self.surface, (255 - round(242 * self.life_time / self.max_life_time),
                                          255 - round(115 * self.life_time / self.max_life_time),
                                          255 - round(43 * self.life_time / self.max_life_time)),
                           (self.rect.width // 2, self.rect.height // 2),
                           round(self.rect.width // 2 * self.life_time / self.max_life_time))
        super().draw(surface)


class CursorFlashes(Particle):

    def __init__(self, x, y, radius, velocity: pygame.math.Vector2,
                 acceleration: pygame.math.Vector2, life_time, color: tuple):
        self.surface = pygame.Surface((radius * 2, radius * 2))
        self.color = color
        super().__init__(x, y, velocity, acceleration, life_time)

    def draw(self, surface: pygame.Surface):
        self.surface.fill('black')
        pygame.draw.circle(self.surface, self.color,
                           (self.rect.width // 2, self.rect.height // 2),
                           round(self.rect.width // 2 * self.life_time / self.max_life_time))
        super().draw(surface)


class ClickRound(Particle):

    def __init__(self, x, y, radius, velocity: pygame.math.Vector2,
                 acceleration: pygame.math.Vector2, life_time):
        self.surface = pygame.Surface((radius * 8, radius * 8))
        super().__init__(x, y, velocity, acceleration, life_time)

    def draw(self, surface: pygame.Surface):
        self.surface.fill('black')
        # pygame.draw.circle(self.surface, 'blue',
        #                    (self.rect.width // 2, self.rect.height // 2),
        #                    self.rect.width // 8)
        pygame.draw.circle(self.surface, 'lightblue',
                           (self.rect.width // 2, self.rect.height // 2),
                           round(self.rect.width // 2 * (self.max_life_time - self.life_time) / self.max_life_time),
                           self.rect.width // 8)
        super().draw(surface)
