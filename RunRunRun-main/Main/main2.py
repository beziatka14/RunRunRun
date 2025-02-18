import pygame
from random import choice, randint

size = width, height = 400, 600
screen = pygame.display.set_mode(size)

# константы
WIDTH = 400
HEIGHT = 600
WIDTH_IN_CELLS = 9
HEIGHT_IN_CELLS = 24
LEFT = 20  # отступ слева
TOP = 60  # отступ сверху
CELL_SIZE = 40
PLAYER_SIZE = 24
SPACE = (CELL_SIZE - PLAYER_SIZE) // 2
SHOW_FROM = 12  # номер линии, начиная с которой игрок может видеть поле
LINES = []  # список хранит объекты класса Line
START_Y = TOP - (HEIGHT_IN_CELLS - SHOW_FROM) * CELL_SIZE
START_FIELD_HEIGHT = 7
MAX_PLAYER_Y = START_Y + (HEIGHT_IN_CELLS - START_FIELD_HEIGHT // 2) * CELL_SIZE
list_for_choice = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3]
# переменные для счета и рекорда
score = 0
max_score = 0


def generate(line, y):  # функция генерации новой линии
    global LINES
    x = LEFT
    if line == 0:
        LINES.append(Normal(y))
        for j in range(WIDTH_IN_CELLS):
            NormalCell(field, x, y)
            x += CELL_SIZE
    elif line == 1:
        LINES.append(Road(y))
        for j in range(WIDTH_IN_CELLS):
            RoadCell(field, x, y)
            x += CELL_SIZE
    elif line == 2:
        LINES.append(River(y))
        for j in range(WIDTH_IN_CELLS):
            RiverCell(field, x, y)
            x += CELL_SIZE
    else:
        LINES.append(Railway(y))
        for j in range(WIDTH_IN_CELLS):
            RailwayCell(field, x, y)
            x += CELL_SIZE


def load_image(name, colorkey=None):
    image = pygame.image.load(name).convert_alpha()
    return image


# Изображения
frame_image = load_image("Images/frame_image.png")
frame_rect = frame_image.get_rect()

player_image_forward = load_image("Images/player_image_forward.png")
player_image_right = load_image("Images/player_image_right.png")
player_image_left = load_image("Images/player_image_left.png")
player_image_backward = load_image("Images/player_image_backward.png")

normal_cell_image = load_image("Images/normal_cell_image.png")
road_cell_image = load_image("Images/road_cell_image.png")
river_cell_image = load_image("Images/river_cell_image.png")
railway_cell_image = load_image("Images/railway_cell_image.png")

car1_image_right = load_image("Images/car1_image_right.png")
car2_image_right = load_image("Images/car2_image_right.png")
car3_image_right = load_image("Images/car3_image_right.png")
car4_image_right = load_image("Images/car4_image_right.png")
car5_image_right = load_image("Images/car5_image_right.png")
car1_image_left = load_image("Images/car1_image_left.png")
car2_image_left = load_image("Images/car2_image_left.png")
car3_image_left = load_image("Images/car3_image_left.png")
car4_image_left = load_image("Images/car4_image_left.png")
car5_image_left = load_image("Images/car5_image_left.png")

boat_image = load_image("Images/boat_image.png")
train_image_rigth = load_image("Images/train_image_right.png")
train_image_left = load_image("Images/train_image_left.png")


# родительский класс клетки
class Cell(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        if args and args[0]:
            self.rect.y += CELL_SIZE
        if self.rect.y > TOP + (HEIGHT_IN_CELLS - SHOW_FROM) * CELL_SIZE:
            self.kill()


class NormalCell(Cell):
    image = normal_cell_image

    def init(self, group, x, y):
        super().__init__(group, x, y)


class RoadCell(Cell):
    image = road_cell_image

    def init(self, group, x, y):
        super().__init__(group, x, y)


class RiverCell(Cell):
    image = river_cell_image

    def init(self, group, x, y):
        super().__init__(group, x, y)


class RailwayCell(Cell):
    image = railway_cell_image

    def init(self, group, x, y):
        super().__init__(group, x, y)


# родительский класс линии
class Line:
    def __init__(self, y, me, move=False):
        self.y = y
        self.me = me
        if move:
            self.course_to_the_right = choice((True, False))
            if self.course_to_the_right:
                self.x = LEFT - CELL_SIZE
            else:
                self.x = LEFT + CELL_SIZE * WIDTH_IN_CELLS
            self.start = pygame.time.get_ticks()
            self.interval = self.interval = randint(0, 5) * 200


class Normal(Line):
    def __init__(self, y):
        self.moving_line = False
        super().__init__(y, 'NORMAL', self.moving_line)


class Road(Line):
    def __init__(self, y):
        self.moving_line = True
        super().__init__(y, 'ROAD', self.moving_line)
        self.speed = randint(2, 3)
        self.create_an_object(self.start)

    def create_an_object(self, time_now):
        if time_now - self.start >= self.interval:
            Car(moving_objects, self.x, self.y, self.course_to_the_right, self.speed)
            self.start = time_now
            self.interval = randint(8, 16) * 250


class River(Line):
    def __init__(self, y):
        self.moving_line = True
        super().__init__(y, 'RIVER', self.moving_line)
        self.speed = 1
        self.create_an_object(self.start)

    def create_an_object(self, time_now):
        if time_now - self.start >= self.interval:
            Boat(moving_objects, self.x, self.y, self.course_to_the_right, self.speed)
            self.start = time_now
            self.interval = randint(8, 40) * 250


class Railway(Line):
    def __init__(self, y):
        self.moving_line = True
        super().__init__(y, 'RAILWAY', self.moving_line)
        if self.course_to_the_right:
            self.x = LEFT - 9 * CELL_SIZE
        else:
            self.x = LEFT + WIDTH_IN_CELLS * CELL_SIZE
        self.speed = 23
        self.interval = randint(4, 7) * 1000

    def create_an_object(self, time_now):
        if time_now - self.start >= self.interval:
            Train(moving_objects, self.x, self.y, self.course_to_the_right, self.speed)
            self.start = time_now
            self.interval = randint(4, 7) * 1000


# классы подвижных объектов
class Car(pygame.sprite.Sprite):
    def __init__(self, group, x, y, course_to_the_right, speed):
        super().__init__(group)
        if course_to_the_right:
            self.image = choice(
                (car1_image_right, car2_image_right, car3_image_right, car4_image_right, car5_image_right))
        else:
            self.image = choice((car1_image_left, car2_image_left, car3_image_left, car4_image_left, car5_image_left))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.course_to_the_right = course_to_the_right
        self.speed = speed

    def update(self, *args):
        if self.course_to_the_right:
            if self.rect.x < LEFT + WIDTH_IN_CELLS * CELL_SIZE:
                self.rect.x += self.speed
            else:
                self.kill()
        else:
            if self.rect.x > LEFT - CELL_SIZE:
                self.rect.x -= self.speed
            else:
                self.kill()
        if args and args[0]:
            self.rect.y += CELL_SIZE
        if self.rect.y > TOP + (HEIGHT_IN_CELLS - SHOW_FROM) * CELL_SIZE:
            self.kill()


class Boat(pygame.sprite.Sprite):
    def __init__(self, group, x, y, course_to_the_right, speed):
        super().__init__(group)
        self.image = boat_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.course_to_the_right = course_to_the_right
        self.speed = speed

    def update(self, *args):
        if self.course_to_the_right:
            if self.rect.x < LEFT + WIDTH_IN_CELLS * CELL_SIZE:
                self.rect.x += self.speed
            else:
                self.kill()
        else:
            if self.rect.x > LEFT - CELL_SIZE:
                self.rect.x -= self.speed
            else:
                self.kill()
        if args and args[0]:
            self.rect.y += CELL_SIZE
        if self.rect.y > TOP + (HEIGHT_IN_CELLS - SHOW_FROM) * CELL_SIZE:
            self.kill()


class Train(pygame.sprite.Sprite):
    def __init__(self, group, x, y, course_to_the_right, speed):
        super().__init__(group)
        if course_to_the_right:
            self.image = train_image_rigth
        else:
            self.image = train_image_left
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.course_to_the_right = course_to_the_right
        self.speed = speed

    def update(self, *args):
        if self.course_to_the_right:
            if self.rect.x < LEFT + WIDTH_IN_CELLS * CELL_SIZE:
                self.rect.x += self.speed
            else:
                self.kill()
        else:
            if self.rect.x > LEFT - 9 * CELL_SIZE:
                self.rect.x -= self.speed
            else:
                self.kill()
        if args and args[0]:
            self.rect.y += CELL_SIZE
        if self.rect.y > TOP + (HEIGHT_IN_CELLS - SHOW_FROM) * CELL_SIZE:
            self.kill()


# класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group)
        self.image = player_image_forward
        self.rect = self.image.get_rect()
        self.rect.x = LEFT + WIDTH_IN_CELLS // 2 * CELL_SIZE + SPACE
        self.rect.y = MAX_PLAYER_Y
        self.line_i = START_FIELD_HEIGHT // 2
        self.boat = None

    def update(self, *args):
        global score, max_score
        running = True
        if LINES[self.line_i].me == 'RIVER':
            self.boat = pygame.sprite.spritecollideany(self, moving_objects)
            if not self.boat:
                running = False
        else:
            if self.boat:
                self.boat = False
            if pygame.sprite.spritecollideany(self, moving_objects):
                running = False

        if self.boat:
            self.rect.x = self.boat.rect.x + 6

        if args:
            course = args[0]
            if course == 'f':
                self.image = player_image_forward
                if self.rect.y != MAX_PLAYER_Y:
                    self.rect.y -= CELL_SIZE
                    self.line_i += 1
                self.rect.x = LEFT + (round((self.rect.x - SPACE - LEFT) / CELL_SIZE)) * CELL_SIZE + SPACE
                score += 1  # увеличение счета
                if score > max_score:
                    max_score = score  # обновление рекорда
            elif course == 'r':
                self.image = player_image_right
                if self.rect.x != LEFT + (WIDTH_IN_CELLS - 1) * CELL_SIZE + SPACE:
                    self.rect.x += CELL_SIZE
            elif course == 'l':
                self.image = player_image_left
                if self.rect.x != LEFT + SPACE:
                    self.rect.x -= CELL_SIZE
            elif course == 'd':
                self.image = player_image_backward
                if self.rect.y < START_Y + HEIGHT_IN_CELLS * CELL_SIZE:
                    self.rect.y += CELL_SIZE
                    self.rect.x = LEFT + (round((self.rect.x - SPACE - LEFT) / CELL_SIZE)) * CELL_SIZE + SPACE
                    self.line_i -= 1
                score = max(0, score - 1)
        return running


# класс меню
class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font("Fonts/pixel_font.otf", 24)  # шрифт для кнопки
        self.pixel_font = pygame.font.Font("Fonts/pixel_font.otf", 40)  # шрифт для заголовка
        self.start_button = pygame.Rect(100, 450, 200, 50)
        self.start_text = self.font.render('Начать игру', True, (255, 255, 255))
        self.start_text_shadow = self.font.render('Начать игру', True, (0, 0, 0))  # тень
        self.start_text_rect = self.start_text.get_rect(center=self.start_button.center)
        self.background = load_image("Images/menu.png")
        self.title_text = self.pixel_font.render('Crossy Road', True, (255, 255, 255))
        self.title_text_shadow = self.pixel_font.render('Crossy Road', True, (0, 0, 0))  # тень
        self.title_text_rect = self.title_text.get_rect(center=(width // 2, 100))
        self.max_score = 0

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        shadow_offset = 2  # смещение тени
        self.screen.blit(self.title_text_shadow,
                         (self.title_text_rect.x + shadow_offset, self.title_text_rect.y + shadow_offset))
        self.screen.blit(self.title_text, self.title_text_rect)

        max_score_text = self.font.render(f'Max Score: {self.max_score}', True,
                                          (255, 255, 255))
        max_score_text_shadow = self.font.render(f'Max Score: {self.max_score}', True, (0, 0, 0))
        max_score_text_rect = max_score_text.get_rect(center=(width // 2, 200))

        # тень
        self.screen.blit(max_score_text_shadow,
                         (max_score_text_rect.x + shadow_offset, max_score_text_rect.y + shadow_offset))
        self.screen.blit(max_score_text, max_score_text_rect)

        pygame.draw.rect(self.screen, (0, 128, 0), self.start_button)

        self.screen.blit(self.start_text_shadow,
                         (self.start_text_rect.x + shadow_offset, self.start_text_rect.y + shadow_offset))
        self.screen.blit(self.start_text, self.start_text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.collidepoint(event.pos):
                return True
        return False


class GameOverScreen:
    def __init__(self, screen, max_score):
        self.screen = screen
        self.max_score = max_score
        self.font = pygame.font.Font("Fonts/pixel_font.otf", 60)
        self.score_font = pygame.font.Font("Fonts/pixel_font.otf", 30)
        self.button_font = pygame.font.Font("Fonts/pixel_font.otf", 24)
        # текст "Game Over" 
        self.game_over_text = self.font.render('Game Over', True, (255, 0, 0))
        self.game_over_text_shadow = self.font.render('Game Over', True, (0, 0, 0))
        self.game_over_text_rect = self.game_over_text.get_rect(center=(width // 2, height // 2 - 50))

        self.max_score_text = self.score_font.render(f'Рекорд: {self.max_score}', True,
                                                     (255, 255, 255))
        self.max_score_text_shadow = self.score_font.render(f'Рекорд: {self.max_score}', True, (0, 0, 0))
        self.max_score_text_rect = self.max_score_text.get_rect(center=(width // 2, height // 2 + 20))

        # кнопка "Начать заново" 
        self.restart_button = pygame.Rect(width // 2 - 150, height // 2 + 80, 300, 50)
        self.restart_text = self.button_font.render('Начать заново', True, (255, 255, 255))
        self.restart_text_shadow = self.button_font.render('Начать заново', True, (0, 0, 0))
        self.restart_text_rect = self.restart_text.get_rect(center=self.restart_button.center)

    def draw(self):
        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))

        shadow_offset = 2
        self.screen.blit(self.game_over_text_shadow,
                         (self.game_over_text_rect.x + shadow_offset, self.game_over_text_rect.y + shadow_offset))
        self.screen.blit(self.game_over_text, self.game_over_text_rect)

        self.screen.blit(self.max_score_text_shadow,
                         (self.max_score_text_rect.x + shadow_offset, self.max_score_text_rect.y + shadow_offset))
        self.screen.blit(self.max_score_text, self.max_score_text_rect)

        pygame.draw.rect(self.screen, (0, 128, 0), self.restart_button)
        self.screen.blit(self.restart_text_shadow,
                         (self.restart_text_rect.x + shadow_offset, self.restart_text_rect.y + shadow_offset))
        self.screen.blit(self.restart_text, self.restart_text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.restart_button.collidepoint(event.pos):
                return True  # True, если кнопка нажата
        return False


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode(size)
    menu = Menu(screen)
    in_menu = True

    while in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                in_menu = False
                running = False
            if menu.handle_event(event):
                in_menu = False
                running = True

        screen.fill((0, 0, 0))
        menu.draw()
        pygame.display.flip()

    while True:
        field = pygame.sprite.Group()
        moving_objects = pygame.sprite.Group()
        player_group = pygame.sprite.Group()

        player = Player()
        y = TOP + (HEIGHT_IN_CELLS - SHOW_FROM + 1) * CELL_SIZE
        for i in range(START_FIELD_HEIGHT):
            line = 0
            y -= CELL_SIZE
            generate(line, y)
        for i in range(HEIGHT_IN_CELLS - START_FIELD_HEIGHT):
            line = choice(list_for_choice)
            y -= CELL_SIZE
            generate(line, y)

        font = pygame.font.Font("Fonts/pixel_font.otf", 16)

        running = True
        while running:
            move = False  # движение поля
            course = 's'  # направление игрока
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        course = 'f'
                        if player.rect.y == MAX_PLAYER_Y:
                            move = True
                            # генерация новой линии
                            generate(choice(list_for_choice), -SHOW_FROM * CELL_SIZE + TOP)
                            # удаление последней линии
                            LINES = LINES[1:]
                    if event.key == pygame.K_RIGHT:
                        course = 'r'
                    if event.key == pygame.K_LEFT:
                        course = 'l'
                    if event.key == pygame.K_DOWN:
                        course = 'd'

            field.update(move)
            moving_objects.update(move)
            running = player.update(course)

            screen.fill((255, 255, 255))
            field.draw(screen)
            moving_objects.draw(screen)
            player_group.draw(screen)
            screen.blit(frame_image, frame_rect)

            # счет и рекорд
            score_text = font.render(f'Score: {score}', True, (255, 255, 255))
            max_score_text = font.render(f'Max Score: {max_score}', True, (255, 255, 255))

            shadow_offset = 2
            screen.blit(font.render(f'Score: {score}', True, (0, 0, 0)), (10 + shadow_offset, 10 + shadow_offset))
            screen.blit(font.render(f'Max Score: {max_score}', True, (0, 0, 0)),
                        (10 + shadow_offset, 35 + shadow_offset))

            screen.blit(score_text, (10, 10))
            screen.blit(max_score_text, (10, 35))

            time_now = pygame.time.get_ticks()
            for i in range(len(LINES)):
                LINES[i].y = START_Y + (HEIGHT_IN_CELLS - i) * CELL_SIZE
                if LINES[i].moving_line:
                    LINES[i].create_an_object(time_now)

            pygame.time.delay(40)
            pygame.display.flip()

        # экран "Game Over"
        game_over_screen = GameOverScreen(screen, max_score)
        game_over = True
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if game_over_screen.handle_event(event):
                    game_over = False  # перезапуск игры
                    field.empty()
                    moving_objects.empty()
                    player_group.empty()
                    LINES.clear()
                    score = 0
                    break

            screen.fill((0, 0, 0))
            game_over_screen.draw()
            pygame.display.flip()