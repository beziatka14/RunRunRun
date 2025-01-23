import pygame
from random import choice


pygame.init()
size = width, height = 400, 600
screen = pygame.display.set_mode(size)

WIDTH = 400
HEIGHT = 600
WIDTH_IN_CELLS = 9
HEIGHT_IN_CELLS = 15
LEFT = 20
TOP = 20
CELL_SIZE = 40
SHOW_FROM = 3
SPEED = 1
list_for_choice = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3]

def generate(line, y):
    x = LEFT
    for j in range(WIDTH_IN_CELLS):
        if line == 0:
            NormalCell(field, x, y)
        elif line == 1:
            RoadCell(field, x, y)
        elif line == 2:
            RiverCell(field, x, y)
        else:
            RailwayCell(field, x, y)
        x += CELL_SIZE




def load_image(name, colorkey=None):
    image = pygame.image.load(name).convert_alpha()
    return image

class Cell(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.rect.y < TOP + (HEIGHT_IN_CELLS - SHOW_FROM) * CELL_SIZE:
            self.rect.y += SPEED
        else:
            self.kill()
            generate(choice(list_for_choice), -SHOW_FROM * CELL_SIZE + TOP)


class NormalCell(Cell):
    image = load_image("../Images/normal_cell_image.png")
    def init(self, group, x, y):
        super().__init__(group, x, y)
        self.image = NormalCell.image


class RoadCell(Cell):
    image = load_image("../Images/road_cell_image.png")
    def init(self, group, x, y):
        super().__init__(group)
        self.image = RoadCell.image


class RiverCell(Cell):
    image = load_image("../Images/river_cell_image.png")

    def init(self, group, x, y):
        super().__init__(group)
        self.image = RiverCell.image


class RailwayCell(Cell):
    image = load_image("../Images/railway_cell_image.png")

    def init(self, group, x, y):
        super().__init__(group)
        self.image = RoadCell.image



if __name__ == "__main__":
    running = True
    screen.fill((255, 255, 255))

    field = pygame.sprite.Group()

    y = -SHOW_FROM * CELL_SIZE + TOP
    for i in range(HEIGHT_IN_CELLS):
        line = choice(list_for_choice)
        y += CELL_SIZE
        generate(line, y)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        field.draw(screen)
        field.update()

        pygame.display.flip()
        pygame.time.delay(50)

    pygame.quit()