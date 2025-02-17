import pygame
from random import choice, randint

size = width, height = 400, 600
screen = pygame.display.set_mode(size)

WIDTH = 400
HEIGHT = 600
WIDTH_IN_CELLS = 10
HEIGHT_IN_CELLS = 24
LEFT = 0
TOP = 0
CELL_SIZE = 40
PLAYER_SIZE = 24
SPACE = (CELL_SIZE - PLAYER_SIZE) // 2
SHOW_FROM = 12
LINES = []
START_Y = TOP - (HEIGHT_IN_CELLS - SHOW_FROM) * CELL_SIZE
START_FIELD_HEIGHT = 6
MAX_PLAYER_Y = TOP + (SHOW_FROM - 4) * CELL_SIZE + SPACE
list_for_choice = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3]


def generate(line, y):
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

player_image_forward = load_image("../Images/player_image_forward.png")
player_image_right = load_image("../Images/player_image_right.png")
player_image_left = load_image("../Images/player_image_left.png")
player_image_backward = load_image("../Images/player_image_backward.png")

normal_cell_image = load_image("../Images/normal_cell_image.png")
road_cell_image = load_image("../Images/road_cell_image.png")
river_cell_image = load_image("../Images/river_cell_image.png")
railway_cell_image = load_image("../Images/railway_cell_image.png")

car1_image = load_image("../Images/car1_image.png")
car2_image = load_image("../Images/car2_image.png")
car3_image = load_image("../Images/car3_image.png")
boat_image = load_image("../Images/boat_image.png")
train_image = load_image("../Images/train_image.png")

class Cell(pygame.sprite.Sprite):

    def __init__(self, group, x, y):
        super().__init__(group)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        if args and args[0]:
            self.rect.y += CELL_SIZE
        # else:
        #     self.rect.y += SPEED
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
            self.interval = 0


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
            self.interval = randint(8, 16) * 250


class Railway(Line):
    def __init__(self, y):
        self.moving_line = True
        super().__init__(y, 'RAILWAY', self.moving_line)
        if self.course_to_the_right:
            self.x = LEFT - 9 * CELL_SIZE
        else:
            self.x = LEFT + WIDTH_IN_CELLS * CELL_SIZE
        self.speed = 23
        self.interval = 3000

    def create_an_object(self, time_now):
        if time_now - self.start >= self.interval:
            Train(moving_objects, self.x, self.y, self.course_to_the_right, self.speed)
            self.start = time_now
            self.interval = randint(4, 7) * 1000


class Car(pygame.sprite.Sprite):
    def __init__(self, group, x, y, course_to_the_right, speed):
        super().__init__(group)
        self.image = choice((car1_image, car2_image, car3_image))
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
        self.image = train_image
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


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(player_group)
        self.image = player_image_forward
        self.rect = self.image.get_rect()
        self.rect.x = LEFT + WIDTH_IN_CELLS // 2 * CELL_SIZE + SPACE
        self.rect.y = MAX_PLAYER_Y
        self.line_i = 4
        self.boat = None

    def update(self, *args):
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
            self.rect.x = self.boat.rect.x + SPACE

        if args:
            course = args[0]
            if course == 'f':
                self.image = player_image_forward
                if self.rect.y != MAX_PLAYER_Y:
                    self.rect.y -= CELL_SIZE
                    self.line_i += 1
                self.rect.x = LEFT + (round((self.rect.x - SPACE - LEFT) / CELL_SIZE)) * CELL_SIZE + SPACE
            elif course == 'r':
                self.image = player_image_right
                if self.rect.x != LEFT + (WIDTH_IN_CELLS - 1) * CELL_SIZE:
                    self.rect.x += CELL_SIZE
            elif course == 'l':
                self.image = player_image_left
                if self.rect.x != LEFT:
                    self.rect.x -= CELL_SIZE
            elif course == 'd':
                self.image = player_image_backward
                if self.rect.y != START_Y + HEIGHT_IN_CELLS * CELL_SIZE:
                    self.rect.y += CELL_SIZE
                    self.rect.x = LEFT + (round((self.rect.x - SPACE - LEFT) / CELL_SIZE)) * CELL_SIZE + SPACE
                    self.line_i -= 1
        # return running
        return True


if __name__ == "__main__":
    pygame.init()

    running = True
    screen.fill((255, 255, 255))

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

    while running:
        move = False
        course = 's'
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    course = 'f'
                    if player.rect.y == MAX_PLAYER_Y:
                        move = True
                        generate(choice(list_for_choice), -SHOW_FROM * CELL_SIZE + TOP)
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
        field.draw(screen)
        moving_objects.draw(screen)
        player_group.draw(screen)

        time_now = pygame.time.get_ticks()
        for i in range(len(LINES)):
            LINES[i].y = START_Y + (HEIGHT_IN_CELLS - i) * CELL_SIZE
            if LINES[i].moving_line:
                LINES[i].create_an_object(time_now)

        pygame.time.delay(40)
        pygame.display.flip()

    if input() == '0':
        pygame.quit()
