from classes.level import *


class Drawing:
    hearts_dict = {i: pygame.image.load(f'resources/images/interface/heart{i}.png').convert_alpha()
                   for i in range(4)}
    empty_heart = pygame.image.load('resources/images/interface/heart_empty.png').convert_alpha()
    coin = pygame.transform.scale(pygame.image.load('resources/images/surrounding/coins/gold_coin_3.png'),
                                  (35, 35)).convert_alpha()
    key = pygame.transform.scale(pygame.image.load('resources/images/surrounding/key.png'),
                                 (35, 35)).convert_alpha()

    def __init__(self, manager: GameManager, level: Level):
        self.manager = manager
        self.surf = manager.surf
        self.level = level
        self.background_surf = pygame.Surface(self.surf.get_size())
        self.background_surf.fill('yellow')
        self.player_score = 0
        self.decor: list[Decor] = []

    def background(self):
        self.surf.blit(self.background_surf, (0, 0))

    def draw_level(self):
        self.level.draw(self.surf)

    def draw_ui(self):

        if self.manager.game_state == 'game':

            if self.level.state == 'game':  # displaying player's stats
                pygame.draw.rect(self.surf, 'black', (-10, -10, DISP_WIDTH // 6 + 10, DISP_HEIGHT // 5 + 30),
                                 border_radius=8)
                pygame.draw.rect(self.surf, '#6c380f', (-10, -10, DISP_WIDTH // 6 - 10, DISP_HEIGHT // 5 + 10),
                                 border_radius=8)
                self.surf.blit(self.coin, (10, 65))
                self.surf.blit(stats_font.render(str(self.player_score), True, 'yellow'), (55, 50))
                if self.level.key_count:
                    self.surf.blit(self.key, (10, 105))
                    self.surf.blit(
                        stats_font.render(f'{self.level.player.keys} / {self.level.key_count}', True, 'grey'),
                        (55, 90))

                for i in range(0, 12, 4):
                    if self.level.player.health >= i + 4:
                        self.surf.blit(self.hearts_dict[0], (5 + i * 15, 5))
                    elif i < self.level.player.health < i + 4:
                        self.surf.blit(self.hearts_dict[self.level.player.health % 4], (5 + i * 15, 5))
                    else:
                        self.surf.blit(self.empty_heart, (5 + i * 15, 5))

            if self.manager.show_debug:  # displaying debug info
                self.surf.blit(info_font.render(f'level_state: {self.level.state}', True, 'red'),
                               (5, 200))
                self.surf.blit(info_font.render(f'FPS: {round(self.manager.clock.get_fps())}',
                                                True, 'red'), (5, 170))

        for ui in self.level.ui_elements.values():
            ui.draw(self.surf)

        for dec in self.decor:
            dec.draw(self.surf)
            dec.update()

        m_x, m_y = pygame.mouse.get_pos()
        m_x = round(m_x / self.manager.res[0] * DISP_WIDTH)
        m_y = round(m_y / self.manager.res[1] * DISP_HEIGHT)
        pygame.draw.polygon(self.surf, self.manager.cursor_color, ((m_x, m_y),
                                                                   (m_x + 9, m_y + 5),
                                                                   (m_x + 25, m_y + 21),
                                                                   (m_x + 30, m_y + 30),
                                                                   (m_x + 21, m_y + 25),
                                                                   (m_x + 5, m_y + 6)))

        pygame.draw.polygon(self.surf, 'black', ((m_x, m_y),
                                                 (m_x + 9, m_y + 5),
                                                 (m_x + 25, m_y + 21),
                                                 (m_x + 30, m_y + 30),
                                                 (m_x + 21, m_y + 25),
                                                 (m_x + 5, m_y + 6)), width=2)

    def update(self):
        if self.manager.game_state == 'game':
            if self.player_score < self.level.player.score:
                self.player_score += 1
            self.player_score = min(self.level.player.score, self.player_score)
        elif self.manager.game_state == 'main_menu':
            m_x, m_y = pygame.mouse.get_pos()
            m_x = round(m_x / self.manager.res[0] * DISP_WIDTH)
            m_y = round(m_y / self.manager.res[1] * DISP_HEIGHT)
            self.decor.append(CursorFlashes(m_x, m_y, randint(4, 6),
                                            pygame.math.Vector2(uniform(-2., 2), falling_momentum),
                                            pygame.math.Vector2(0, 0),
                                            randint(20, 25), self.manager.cursor_color))
        self.decor = list(filter(lambda i: i.life_time, self.decor))

    def draw(self):
        self.background()
        self.draw_level()
        self.draw_ui()
        self.update()
        self.manager.display.blit(pygame.transform.scale(self.surf, self.manager.res), (0, 0))
