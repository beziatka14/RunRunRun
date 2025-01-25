import pygame
from random import choice, randint

size = width, height = 400, 600
screen = pygame.display.set_mode(size)

WIDTH = 400
HEIGHT = 600
WIDTH_IN_CELLS = 9
HEIGHT_IN_CELLS = 20
LEFT = 20
TOP = 20
CELL_SIZE = 40
SHOW_FROM = 8
ROADS = []
list_for_choice = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3]


def generate(line, y):
    x = LEFT
    if line == 0:
        for j in range(WIDTH_IN_CELLS):
            NormalCell(field, x, y)
            x += CELL_SIZE
    elif line == 1:
        ROADS.append(Road(y))
        for j in range(WIDTH_IN_CELLS):
            RoadCell(field, x, y)
            x += CELL_SIZE
    elif line == 2:
        for j in range(WIDTH_IN_CELLS):
            RiverCell(field, x, y)
            x += CELL_SIZE
    else:
        for j in range(WIDTH_IN_CELLS):
            RailwayCell(field, x, y)
            x += CELL_SIZE


def load_image(name, colorkey=None):
    image = pygame.image.load(name).convert_alpha()
    return image


normal_cell_image = load_image("../Images/normal_cell_image.png")
road_cell_image = load_image("../Images/road_cell_image.png")
river_cell_image = load_image("../Images/river_cell_image.png")
railway_cell_image = load_image("../Images/railway_cell_image.png")
car1_image = load_image("../Images/car1_image.png")
car2_image = load_image("../Images/car2_image.png")
car3_image = load_image("../Images/car3_image.png")


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


class Road:
    def __init__(self, y):
        self.y = y
        self.course_to_the_right = choice((True, False))
        self.speed = randint(1, 3)
        self.start_of_timer = pygame.time.get_ticks()
        self.interval = 0
        self.create_a_car()

    def update(self, move):
        if pygame.time.get_ticks() - self.start_of_timer >= self.interval:
            self.create_a_car()
        if move:
            self.y += CELL_SIZE
            if self.y >= TOP + (HEIGHT_IN_CELLS - SHOW_FROM) * CELL_SIZE:
                del ROADS[0]

    def create_a_car(self):
        self.start_of_timer = pygame.time.get_ticks()
        if self.course_to_the_right:
            x = LEFT - CELL_SIZE
        else:
            x = LEFT + CELL_SIZE * WIDTH_IN_CELLS
        Car(self, cars, x)

        self.interval = randint(2, 5) * 1000


class Car(pygame.sprite.Sprite):
    def __init__(self, road, group, x):
        super().__init__(group)
        self.image = choice((car1_image, car2_image, car3_image))
        self.rect = self.image.get_rect()
        self.road = road
        self.rect.x = x
        self.rect.y = self.road.y

    def update(self, *args):
        if self.road.course_to_the_right:
            if self.rect.x < LEFT + WIDTH_IN_CELLS * CELL_SIZE:
                self.rect.x += self.road.speed
            else:
                self.kill()
        else:
            if self.rect.x > LEFT - CELL_SIZE:
                self.rect.x -= self.road.speed
            else:
                self.kill()
        if args and args[0]:
            self.rect.y += CELL_SIZE
        if self.rect.y > TOP + (HEIGHT_IN_CELLS - SHOW_FROM) * CELL_SIZE:
            self.kill()


if __name__ == "__main__":
    pygame.init()

    running = True
    screen.fill((255, 255, 255))

    field = pygame.sprite.Group()
    cars = pygame.sprite.Group()

    y = -SHOW_FROM * CELL_SIZE + TOP
    for i in range(HEIGHT_IN_CELLS):
        line = choice(list_for_choice)
        y += CELL_SIZE
        generate(line, y)

    while running:
        move = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    move = True
                    generate(choice(list_for_choice), -SHOW_FROM * CELL_SIZE + TOP)
        for road in ROADS:
            road.update(move)
        field.update(move)
        field.draw(screen)
        cars.update(move)
        cars.draw(screen)
        pygame.time.delay(40)
        pygame.display.flip()

    pygame.quit()
