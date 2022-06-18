from classes.player import *

class Block:

    surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))

    def __init__(self, x, y):

        self.cur_rect = self.surface.get_rect(topleft=(x * BLOCK_SIZE, y * BLOCK_SIZE))
        self.surface.fill('blue')

    def collide(self, entity: Player):

        if entity.cur_rect.colliderect(self.cur_rect):

            # left side
            if entity.cur_rect.right >= self.cur_rect.left >= entity.prev_rect.right:
                entity.cur_rect.right = self.cur_rect.left
                entity.collided_sides['right'] = True

            # right side
            elif entity.cur_rect.left <= self.cur_rect.right <= entity.prev_rect.left:
                entity.cur_rect.left = self.cur_rect.right
                entity.collided_sides['left'] = True

            # top side
            if entity.cur_rect.bottom >= self.cur_rect.top >= entity.prev_rect.bottom:
                entity.cur_rect.bottom = self.cur_rect.top
                entity.collided_sides['down'] = True

            # bottom side
            elif entity.cur_rect.top <= self.cur_rect.bottom <= entity.prev_rect.top:
                entity.cur_rect.top = self.cur_rect.bottom
                entity.collided_sides['top'] = True


    def draw(self, surface: pygame.Surface):
        surface.blit(self.surface, self.cur_rect)