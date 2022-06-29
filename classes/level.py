from classes.surroundings import *

class Camera:
    # TODO implement changing of display_size with working resizing of surface
    def __init__(self, surf: pygame.Surface):
        self.surf = surf
        self.offset = pygame.math.Vector2(0, 0)
        self.display_size = pygame.math.Vector2(DISP_WIDTH, DISP_HEIGHT)

    def scroll(self, player: Player) -> tuple:
        self.offset.x = min(max(0, player.rect.centerx - self.display_size.x // 2),
                            self.surf.get_width() - self.display_size.x)
        self.offset.y = min(max(0, player.rect.centery - self.display_size.y // 2),
                            self.surf.get_height() - self.display_size.y)
        return self.offset.x, self.offset.y, self.display_size.x, self.display_size.y


class Level:
    # TODO implement camera scrolling from top to bottom of the self at the beginning
    def __init__(self, num, walls: list[Block], moving_obj: list[MovingPlatform], decor: list[Decor],
                 surface: pygame.Surface, start_pos: tuple[int, int], end_level: LevelEnd):
        self.num = num
        self.blocks = walls
        self.moving_obj = moving_obj
        self.decor = decor
        self.surf = surface
        self.surf.set_colorkey('yellow')
        self.camera = Camera(surface)
        self.projectiles: list[Projectile] = []
        self.player = Player(*start_pos)
        self.level_end = end_level

    def draw(self, surface: pygame.Surface):
        self.surf.fill('yellow')


        for obj in self.blocks + self.moving_obj + self.projectiles + self.decor:
            obj.draw(self.surf)

        self.level_end.draw(self.surf)
        self.player.draw(self.surf)
        camera_surf = pygame.Surface(self.camera.display_size)
        camera_surf.fill('yellow')
        camera_surf.set_colorkey('yellow')
        camera_surf.blit(self.surf, (0, 0), self.camera.scroll(self.player))
        surface.blit(pygame.transform.scale(camera_surf, (DISP_WIDTH, DISP_HEIGHT)), (0, 0))

    # TODO try to solve problem connected with collisions and movement
    def physics(self, entities: list[Player], dt):
        for plat in self.moving_obj:
            plat.move()

        for proj in self.projectiles:
            proj.move()
            for block in self.blocks:
                proj.collide(block)

        if dt <= 3:
            for entity in entities:
                entity.vert_move(dt)
                for wall in self.blocks + self.moving_obj:
                    wall.collide(entity, 'h')
                entity.hor_move(dt)
                for wall in self.blocks + self.moving_obj:
                    wall.collide(entity, 'v')
                entity.rect.x = min(max(entity.rect.x, 0), self.surf.get_width() - self.player.rect.width)
                entity.rect.y = min(max(entity.rect.y, 0), self.surf.get_height()- self.player.rect.height)

    def game_cycle(self, surface: pygame.Surface, dt) -> bool:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

                elif event.key == pygame.K_e:
                    self.projectiles.append(self.player.shoot())

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.camera.display_size.x = min(self.camera.display_size.x + 100, self.surf.get_width())
                    self.camera.display_size.y = min(self.camera.display_size.y + 100, self.surf.get_height())
                elif event.button == 5:
                    self.camera.display_size.x = max(self.camera.display_size.x - 100, DISP_WIDTH - 500)
                    self.camera.display_size.y = max(self.camera.display_size.y - 100, DISP_HEIGHT - 500)

        self.draw(surface)


        self.player.get_angle(self.camera.offset)
        self.physics([self.player], dt)
        surface.blit(info_font.render(str(round(degrees(self.player.angle))), True, 'black'),
                     (30, 30))
        surface.blit(info_font.render(f'({round(self.player.velocity.x, 2)}, {round(self.player.velocity.y, 2)})',
                                      True, 'black'),
                     (30, 80))
        surface.blit(info_font.render(f'({round(self.player.acceleration.x, 2)},{round(self.player.acceleration.y, 2)})'
                                      , True, 'black'),
                     (30, 130))
        surface.blit(info_font.render(f'{self.player.air_time}', True, 'black'),
                     (30, 180))
        self.player.update(dt)

        self.clear()
        return self.level_end.update(self.player)

    def clear(self):
        self.projectiles = list(filter(lambda i: not i.collided,
                                       self.projectiles))
