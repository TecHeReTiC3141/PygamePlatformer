from classes.surroundings import *
from classes.ui_elements import *

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
    possible_states = ['scrolling', 'game', 'pause_menu']

    def __init__(self, num, walls: list[Block], obstacles: list[Obstacle], collectable: list[Collectable],
                 decor: list[Decor], entities: list[Entity], surface: pygame.Surface, background_surf: pygame.Surface,
                 start_pos: tuple[int, int], key_count, end_level: LevelEnd, game_manager: GameManager):
        self.num = num
        self.blocks = walls
        self.obstacles = obstacles
        self.collectable = collectable
        self.decor = decor
        self.entities = entities
        self.surf = surface
        self.surf.set_colorkey('yellow')
        self.aspect_ratio = max(self.surf.get_width(), self.surf.get_height()) / \
                            min(self.surf.get_width(), self.surf.get_height())

        self.ui_elements: dict[str, UI] = {
            'skip_scrolling': DirectionButton(DISP_WIDTH - 200, 30, (70, 70), 'r' if self.surf.get_width() >
                                                                                     self.surf.get_width() else 'd'),
            'pause_button': PauseButton(DISP_WIDTH - 100, 30, (70, 70)),
            'pause_menu': PauseMenu(DISP_WIDTH // 4, -360, (640, 360),
                                    [
                                        QuitButton(70, 210, (140, 140)),
                                        SettingsButton(250, 210, (140, 140)),
                                        UnpauseButton(430, 210, (140, 140), 'game'),
                                    ], (DISP_WIDTH // 2, DISP_HEIGHT // 2), f'Level {self.num}', 0)
        }
        self.game_manager = game_manager
        self.background_surf = background_surf
        self.background_surf.set_colorkey('black')

        self.camera = Camera(surface)
        self.projectiles: list[Projectile] = []

        self.player = Player(*start_pos)
        for entity in self.entities:
            entity.target = self.player
        self.last_checkpoint = self.player.rect.center

        self.key_count = key_count
        self.level_end = end_level
        self.level_end.key_count = key_count

        self.init_time = time()
        self.state = 'scrolling'

    def draw(self, surface: pygame.Surface):

        self.surf.fill('yellow')

        for obj in self.blocks + self.collectable + self.obstacles \
                   + self.projectiles + self.decor + self.entities:
            if isinstance(obj, Collectable) and not obj.alive:
                continue
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

        elif self.state == 'pause':
            camera_surf.blit(self.background_surf, (0, 0), self.camera.free_scroll())
            camera_surf.blit(self.surf, (0, 0), self.camera.free_scroll())
            camera_surf.blit(pygame.transform.scale(blur, self.surf.get_size()), (0, 0))

        surface.blit(pygame.transform.scale(camera_surf, (DISP_WIDTH, DISP_HEIGHT)), (0, 0))

    def physics(self, dt):

        for obj in self.obstacles + self.collectable:
            if isinstance(obj, Collectable) and not obj.alive:
                continue
            obj.interact(self.player)

        for proj in self.projectiles:
            for obst in self.blocks + self.obstacles + \
                        self.projectiles + self.entities + [self.player]:
                if type(obst) == type(proj):
                    continue
                elif isinstance(obst, Entity) and obst.hit_cooldown > 0:
                    continue
                coll = proj.interact(obst)
                if coll and isinstance(obst, Entity) and \
                        (not obst.has_hit_cooldown or obst.hit_cooldown <= 0):
                    obst.hurt(proj.damage)
                    obst.rect.x += proj.vector.x * proj.speed * 2

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

    def change_state(self, new_state: str):
        if self.state == 'scrolling':
            if new_state == 'game':
                self.camera.display_size = pygame.math.Vector2(DISP_WIDTH, DISP_HEIGHT)
                self.ui_elements.pop('skip_scrolling')

            elif new_state == 'pause':
                self.ui_elements['unpause_button'] = UnpauseButton(*self.ui_elements['pause_button'].rect.topleft,
                                                                   self.ui_elements['pause_button'].rect.size,
                                                                   self.state)
                self.ui_elements.pop('pause_button')
                self.ui_elements['pause_menu'].active = True

        elif self.state == 'game':
            if new_state == 'pause':
                self.ui_elements['unpause_button'] = UnpauseButton(*self.ui_elements['pause_button'].rect.topleft,
                                                                   self.ui_elements['pause_button'].rect.size,
                                                                   self.state)
                self.ui_elements.pop('pause_button')
                self.ui_elements['pause_menu'].active = True
                self.ui_elements['pause_menu'].time = time() - self.init_time

        elif self.state == 'pause':
            if new_state in ['game', 'scrolling']:
                self.ui_elements['pause_button'] = PauseButton(*self.ui_elements['unpause_button'].rect.topleft,
                                                               self.ui_elements['unpause_button'].rect.size)
                self.ui_elements.pop('unpause_button')
                self.ui_elements['pause_menu'].active = False
        print(self.ui_elements)
        print(self.state, new_state)
        self.state = new_state

    def game_cycle(self, dt) -> bool:

        if self.state == 'scrolling':
            if self.surf.get_width() >= self.surf.get_height():
                self.camera.move('h', round(4 * self.aspect_ratio))
                if self.camera.offset.x + \
                        self.camera.display_size.x >= self.surf.get_width():
                    self.change_state('game')
            else:
                self.camera.move('v', round(4 * self.aspect_ratio))
                if self.camera.offset.y + \
                        self.camera.display_size.y >= self.surf.get_height():
                    self.change_state('game')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if self.state == 'game':
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()

                    elif event.key == pygame.K_e:
                        if self.player.shoot_cooldown <= 0:
                            self.projectiles.append(self.player.shoot())

                    elif event.key == pygame.K_o and self.level_end.active:
                        return True

            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    for ui in list(self.ui_elements.values()):
                        if not ui.rect.collidepoint(pygame.mouse.get_pos()):
                            continue

                        if isinstance(ui, Button):
                            if isinstance(ui, ChangeStateButton):
                                if isinstance(ui, LevelChangeStateButton):
                                    self.change_state(ui.state)
                                elif isinstance(ui, GameChangeStateButton):
                                    self.game_manager.state = ui.state

                        elif isinstance(ui, UI_container) and ui.active:

                            for ui_el in ui.content:
                                if not ui_el.rect.collidepoint(pygame.mouse.get_pos()):
                                    continue
                                if isinstance(ui_el, Button):
                                    if isinstance(ui_el, ChangeStateButton):
                                        if isinstance(ui_el, LevelChangeStateButton):
                                            self.change_state(ui_el.state)
                                        elif isinstance(ui_el, GameChangeStateButton):
                                            self.game_manager.state = ui_el.state

                elif event.button == 4 and self.state == 'game':
                    if self.surf.get_width() <= self.surf.get_height():
                        self.camera.display_size.x = max(self.camera.display_size.x - 100, DISP_WIDTH - 500)
                        self.camera.display_size.y = max(self.camera.display_size.x / ASPECT_RATIO,
                                                         DISP_HEIGHT - 500 / ASPECT_RATIO)
                    else:
                        self.camera.display_size.y = max(self.camera.display_size.y - 100,
                                                         DISP_HEIGHT - 500 / ASPECT_RATIO)
                        self.camera.display_size.x = max(self.camera.display_size.y * ASPECT_RATIO,
                                                         DISP_WIDTH - 500)
                elif event.button == 5 and self.state == 'game':
                    if self.surf.get_width() <= self.surf.get_height():
                        self.camera.display_size.x = min(self.camera.display_size.x + 100, self.surf.get_width(),
                                                         DISP_WIDTH * 2)
                        self.camera.display_size.y = min(self.camera.display_size.x / ASPECT_RATIO,
                                                         self.surf.get_height(), DISP_HEIGHT * 2)
                    else:
                        self.camera.display_size.y = min(self.camera.display_size.y + 100, self.surf.get_height(),
                                                         DISP_HEIGHT * 2)
                        self.camera.display_size.x = min(self.camera.display_size.y * ASPECT_RATIO,
                                                         self.surf.get_width(), DISP_WIDTH * 2)

        self.player.get_angle(self.camera.offset, self.camera.display_size)

        if self.player.rect.y >= self.surf.get_height():
            self.player.health = 0

        if self.player.health <= 0:
            self.player.health = self.player.max_health
            self.player.score = 0
            self.player.keys = 0
            self.player.rect.center = self.last_checkpoint
            for obj in self.collectable:
                obj.alive = True

        if self.state == 'game':
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


class Drawing:
    hearts_dict = {i: pygame.image.load(f'resources/images/interface/heart{i}.png').convert_alpha()
                   for i in range(4)}
    empty_heart = pygame.image.load('resources/images/interface/heart_empty.png').convert_alpha()
    coin = pygame.transform.scale(pygame.image.load('resources/images/surrounding/coins/gold_coin_3.png'),
                                  (35, 35)).convert_alpha()
    key = pygame.transform.scale(pygame.image.load('resources/images/surrounding/key.png'),
                                 (35, 35)).convert_alpha()

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

    # TODO draw main menu and kinda levels map
    def draw_ui(self):
        if self.level.state == 'game':
            pygame.draw.rect(self.surf, 'black', (-10, -10, DISP_WIDTH // 6 + 10, DISP_HEIGHT // 5 + 30),
                             border_radius=8)
            pygame.draw.rect(self.surf, '#6c380f', (-10, -10, DISP_WIDTH // 6 - 10, DISP_HEIGHT // 5 + 10),
                             border_radius=8)
            self.surf.blit(self.coin, (10, 65))
            self.surf.blit(stats_font.render(str(self.player_score), True, 'yellow'), (55, 50))
            if self.level.key_count:
                self.surf.blit(self.key, (10, 105))
                self.surf.blit(stats_font.render(f'{self.level.player.keys} / {self.level.key_count}', True, 'grey'),
                               (55, 90))

            for i in range(0, 12, 4):
                if self.level.player.health >= i + 4:
                    self.surf.blit(self.hearts_dict[0], (5 + i * 15, 5))
                elif i < self.level.player.health < i + 4:
                    self.surf.blit(self.hearts_dict[self.level.player.health % 4], (5 + i * 15, 5))
                else:
                    self.surf.blit(self.empty_heart, (5 + i * 15, 5))
        self.surf.blit(stats_font.render(f'level_state - {self.level.state}', True, 'black'),
                       (5, DISP_HEIGHT // 4))
        for ui in self.level.ui_elements.values():
            ui.draw(self.surf)

    def update(self):
        if self.player_score < self.level.player.score:
            self.player_score += 1

    def draw(self):
        self.background()
        self.draw_level()
        self.draw_ui()
        self.update()
