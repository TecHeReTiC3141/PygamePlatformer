from classes.surroundings import *


class Camera:

    def __init__(self, surf: pygame.Surface):
        self.surf = surf
        self.offset = pygame.math.Vector2(0, 0)
        width, height = surf.get_size()
        if width >= height:

            self.display_size = pygame.math.Vector2(int(height * ASPECT_RATIO), height)
        else:
            self.display_size = pygame.math.Vector2(width, int(width / ASPECT_RATIO))

    def scroll(self, player: Player) -> tuple:
        self.offset.x = min(max(0, player.rect.centerx - self.display_size.x // 2),
                            self.surf.get_width() - self.display_size.x)
        self.offset.y = min(max(0, player.rect.centery - self.display_size.y // 2),
                            self.surf.get_height() - self.display_size.y)
        return self.offset.x, self.offset.y, self.display_size.x, self.display_size.y

    def free_scroll(self) -> tuple:
        return self.offset.x, self.offset.y, self.display_size.x, self.display_size.y

    def move(self, dir: str, speed=5) -> None:
        if dir == 'v':
            self.offset.y = min(self.offset.y + speed, self.surf.get_height() - self.display_size.y)
        elif dir == 'h':
            self.offset.x = min(self.offset.x + speed, self.surf.get_width() - self.display_size.x)


class Level:
    possible_states = ['scrolling', 'game']

    def __init__(self, num, walls: list[Block], obstacles: list[Obstacle], collectable: list[Collectable],
            decor: list[Decor], surface: pygame.Surface, start_pos: tuple[int, int], end_level: LevelEnd):
        self.num = num
        self.blocks = walls
        self.obstacles = obstacles
        self.collectable = collectable
        self.decor = decor
        self.surf = surface
        self.surf.set_colorkey('yellow')
        self.camera = Camera(surface)
        self.projectiles: list[Projectile] = []

        self.player = Player(*start_pos)
        self.last_checkpoint = start_pos
        self.level_end = end_level

        self.state = 'scrolling'

    def draw(self, surface: pygame.Surface):
        self.surf.fill('yellow')

        for obj in self.blocks + self.collectable + self.obstacles \
                   + self.projectiles + self.decor:
            obj.draw(self.surf)

        self.level_end.draw(self.surf)
        self.player.draw(self.surf)
        camera_surf = pygame.Surface(self.camera.display_size)
        camera_surf.fill('yellow')
        camera_surf.set_colorkey('yellow')
        if self.state == 'scrolling':
            camera_surf.blit(self.surf, (0, 0), self.camera.free_scroll())

        elif self.state == 'game':
            camera_surf.blit(self.surf, (0, 0), self.camera.scroll(self.player))
        surface.blit(pygame.transform.scale(camera_surf, (DISP_WIDTH, DISP_HEIGHT)), (0, 0))

    # TODO try to solve problem connected with collisions and movement
    def physics(self, entities: list[Player], dt):

        for entity in entities:
            for obj in self.obstacles + self.collectable:
                obj.interact(entity)

        for proj in self.projectiles:
            for block in self.blocks + self.obstacles:
                proj.interact(block)

        if dt <= 3:
            for entity in entities:
                if self.state == 'game':
                    entity.vert_move(dt)
                for wall in self.blocks + self.obstacles:
                    wall.collide(entity, 'h')
                if self.state == 'game':
                    entity.hor_move(dt)
                for wall in self.blocks + self.obstacles:
                    wall.collide(entity, 'v')
                entity.rect.x = min(max(entity.rect.x, 0), self.surf.get_width() - self.player.rect.width)

    def game_cycle(self, surface: pygame.Surface, dt) -> bool:
        self.draw(surface)

        if self.state == 'scrolling':
            if self.surf.get_width() >= self.surf.get_height():
                self.camera.move('h')
                if self.camera.offset.x + \
                        self.camera.display_size.x >= self.surf.get_width():
                    self.state = 'game'
                    self.camera.display_size = pygame.math.Vector2(DISP_WIDTH, DISP_HEIGHT)
            else:
                self.camera.move('v')
                if self.camera.offset.y + \
                        self.camera.display_size.y >= self.surf.get_height():
                    self.state = 'game'
                    self.camera.display_size = pygame.math.Vector2(DISP_WIDTH, DISP_HEIGHT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if self.state == 'game':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()

                    elif event.key == pygame.K_e:
                        self.projectiles.append(self.player.shoot())

                    elif event.key == pygame.K_o and self.level_end.active:
                        return True

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        if self.surf.get_width() <= self.surf.get_height():
                            self.camera.display_size.x = max(self.camera.display_size.x - 100, DISP_WIDTH - 500)
                            self.camera.display_size.y = max(self.camera.display_size.x / ASPECT_RATIO,
                                                             DISP_HEIGHT - 500 / ASPECT_RATIO)
                        else:
                            self.camera.display_size.y = max(self.camera.display_size.y - 100,
                                                             DISP_HEIGHT - 500 / ASPECT_RATIO)
                            self.camera.display_size.x = max(self.camera.display_size.y * ASPECT_RATIO,
                                                             DISP_WIDTH - 500)
                    elif event.button == 5:
                        if self.surf.get_width() <= self.surf.get_height():
                            self.camera.display_size.x = min(self.camera.display_size.x + 100, self.surf.get_width())
                            self.camera.display_size.y = min(self.camera.display_size.x / ASPECT_RATIO,
                                                             self.surf.get_height())
                        else:
                            self.camera.display_size.y = min(self.camera.display_size.y + 100, self.surf.get_height())
                            self.camera.display_size.x = min(self.camera.display_size.y * ASPECT_RATIO,
                                                             self.surf.get_width())

        self.player.get_angle(self.camera.offset)

        self.physics([self.player], dt)
        if self.player.rect.y >= self.surf.get_height():
            self.player.lives -= 1
            self.player.rect.center = self.last_checkpoint

        self.player.update(dt)
        self.update()
        self.clear()
        self.level_end.interact(self.player)

    # updating of game objects
    def update(self):
        for obj in self.obstacles + self.projectiles + self.collectable:
            obj.update()

    def clear(self):
        self.projectiles = list(filter(lambda i: i.alive,
                                       self.projectiles))

        self.collectable = list(filter(lambda i: i.alive, self.collectable))



class Drawing:

    def __init__(self, surf: pygame.Surface, level: Level):
        self.surf = surf
        self.level = level
        self.background_surf = pygame.Surface(self.surf.get_size())
        self.background_surf.fill('grey')

    def background(self):
        self.surf.blit(self.background_surf, (0, 0))

    def draw_level(self):
        pass
        # surface.blit(info_font.render(str(round(degrees(self.player.angle))), True, 'black'),
        #              (30, 30))
        # surface.blit(info_font.render(f'({round(self.player.velocity.x, 2)}, {round(self.player.velocity.y, 2)})',
        #                               True, 'black'),
        #              (30, 80))
        # surface.blit(info_font.render(f'({round(self.player.acceleration.x, 2)},{round(self.player.acceleration.y, 2)})'
        #                               , True, 'black'),
        #              (30, 130))
        # surface.blit(info_font.render(f'{self.camera.scroll(self.player)}', True, 'black'),
        #              (30, 180))
