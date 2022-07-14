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
                 decor: list[Decor], entities: list[Entity], surface: pygame.Surface, background_surf: pygame.Surface,
                 start_pos: tuple[int, int], end_level: LevelEnd):
        self.num = num
        self.blocks = walls
        self.obstacles = obstacles
        self.collectable = collectable
        self.decor = decor
        self.entities = entities
        self.surf = surface
        self.surf.set_colorkey('yellow')

        self.background_surf = background_surf
        self.background_surf.set_colorkey('black')
        self.camera = Camera(surface)
        self.projectiles: list[Projectile] = []

        self.player = Player(*start_pos)
        for entity in self.entities:
            entity.target = self.player
        self.last_checkpoint = self.player.rect.center
        self.level_end = end_level

        self.state = 'scrolling'

    def draw(self, surface: pygame.Surface):

        self.surf.fill('yellow')

        for obj in self.blocks + self.collectable + self.obstacles \
                   + self.projectiles + self.decor + self.entities:
            obj.draw(self.surf)

        self.level_end.draw(self.surf)
        self.player.draw(self.surf)

        camera_surf = pygame.Surface(self.camera.display_size)
        camera_surf.set_colorkey('yellow')
        camera_surf.fill('yellow')

        if self.state == 'scrolling':
            camera_surf.blit(self.background_surf, (0, 0), self.camera.free_scroll())
            camera_surf.blit(self.surf, (0, 0), self.camera.free_scroll())

        elif self.state == 'game':
            camera_surf.blit(self.background_surf, (0, 0), self.camera.scroll(self.player))
            camera_surf.blit(self.surf, (0, 0), self.camera.scroll(self.player))

        surface.blit(pygame.transform.scale(camera_surf, (DISP_WIDTH, DISP_HEIGHT)), (0, 0))

    def physics(self, dt):

        for obj in self.obstacles + self.collectable:
            obj.interact(self.player)

        for proj in self.projectiles:
            for obst in self.blocks + self.obstacles + self.entities + [self.player]:
                coll = proj.interact(obst)
                if coll and isinstance(obst, Entity) and \
                        (not obst.has_hit_cooldown or obst.hit_cooldown <= 0):
                    obst.hurt(proj.damage)

        if dt <= 3:
            self.player.prev_rect = self.player.rect.copy()
            if self.state == 'game':
                self.player.vert_move(dt)
            for wall in self.blocks + self.obstacles:
                wall.collide(self.player, 'h')
            if self.state == 'game':
                self.player.hor_move(dt)
            for wall in self.blocks + self.obstacles:
                wall.collide(self.player, 'v')
            self.player.rect.x = min(max(self.player.rect.x, 0), self.surf.get_width() - self.player.rect.width)
            self.player.rect.y = max(self.player.rect.y, 0)

    # TODO introduce entities into game cycle
    def game_cycle(self, dt) -> bool:

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

        self.player.get_angle(self.camera.offset, self.camera.display_size)

        if self.player.rect.y >= self.surf.get_height():
            self.player.health = 0

        if self.player.health <= 0:
            self.player.health = self.player.max_health
            self.player.rect.center = self.last_checkpoint

        self.player.update(dt)
        self.physics(dt)
        self.update()

        self.clear()
        self.level_end.interact(self.player)

    # updating of game objects
    def update(self):
        for obj in self.obstacles + self.projectiles + self.collectable + self.entities:
            if isinstance(obj, Cannon):
                proj = obj.update()
                if proj:
                    self.projectiles.append(proj)
            else:
                obj.update()

    def clear(self):
        self.projectiles = list(filter(lambda i: i.alive,
                                       self.projectiles))

        self.collectable = list(filter(lambda i: i.alive, self.collectable))


class Drawing:
    hearts_dict = {i: pygame.image.load(f'resources/images/interface/heart{i}.png').convert_alpha()
                   for i in range(4)}
    empty_heart = pygame.image.load('resources/images/interface/heart_empty.png').convert_alpha()

    def __init__(self, surf: pygame.Surface, level: Level):
        self.surf = surf
        self.level = level
        self.background_surf = pygame.Surface(self.surf.get_size())
        self.background_surf.fill('black')
        self.player_score = 0

    def background(self):
        self.surf.blit(self.background_surf, (0, 0))

    def draw_level(self):
        self.level.draw(self.surf)

    # TODO draw main menu, pause menu and kinda levels map
    def draw_player_stats(self):
        if self.level.state == 'game':
            pygame.draw.rect(self.surf, 'black', (0, 0, DISP_WIDTH // 5 + 20, DISP_HEIGHT // 6 + 20))
            pygame.draw.rect(self.surf, '#6c380f', (0, 0, DISP_WIDTH // 5, DISP_HEIGHT // 6))
            self.surf.blit(stats_font.render(f'Score: {self.player_score}', True, 'yellow'), (5, 65))
            for i in range(0, 12, 4):
                if self.level.player.health >= i + 4:
                    self.surf.blit(self.hearts_dict[0], (5 + i * 15, 15))
                elif i < self.level.player.health < i + 4:
                    self.surf.blit(self.hearts_dict[self.level.player.health % 4], (5 + i * 15, 15))
                else:
                    self.surf.blit(self.empty_heart, (5 + i * 15, 15))

    def update(self):
        if self.player_score < self.level.player.score:
            self.player_score += 1

    def draw(self):
        self.background()
        self.draw_level()
        self.draw_player_stats()
        self.update()
