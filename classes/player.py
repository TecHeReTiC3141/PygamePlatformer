from scripts.const import *


class Player:

    sprites: dict[str, pygame.Surface] \
        = {i: pygame.image.load(f'resources/images/entities/heretic/heretic_sprite_{i}.png')
               for i in directions}
    size = (75, 100)

    jump_strength = 15
    max_jump_cooldown = 30

    def __init__(self, x, y, ):
        self.surface = pygame.Surface(self.size)
        self.cur_rect = self.surface.get_rect(topleft=(x, y))
        self.prev_rect = self.cur_rect.copy()
        self.movement = pygame.math.Vector2(0, 0)
        self.direction = 'left'
        self.speed = 8
        self.jump_cooldown = 0

        self.collided_sides = {i: False for i in directions}

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.movement.x -= 1
        if keys[pygame.K_d]:
            self.movement.x += 1

    def update(self):

        self.prev_rect = self.cur_rect.copy()
        self.move()
        if self.movement.length():
            norm_move = self.movement.normalize()
            self.cur_rect.move_ip(norm_move * self.speed)
        if self.movement.x > 0:
            self.direction = 'right'
        elif self.movement.x < 0:
            self.direction = 'left'

        self.movement.x = 0
        self.movement.y = min(self.movement.y + .8, .8 if not self.collided_sides['down'] else 0)
        for dir in self.collided_sides:
            self.collided_sides[dir] = False

        self.jump_cooldown -= 1


    def jump(self):
        if self.jump_cooldown <= 0:
            self.movement.y = -self.jump_strength
            self.jump_cooldown = self.max_jump_cooldown

    def draw(self, surface: pygame.Surface):

        self.surface.blit(self.sprites[self.direction], (0, 0))
        surface.blit(self.surface, self.cur_rect)
