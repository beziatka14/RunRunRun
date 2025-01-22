import pygame
from random import choice

def generate():
    list_for_choice = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3]
    ch = choice(list_for_choice)
    if ch == 0:
        new_line = Normal(...)
    elif ch == 1:
        new_line = Car(...)
    elif ch == 2:
        new_line = River(...)
    else:
        new_line = Train(...)
    return new_line

class Board:
    def init(self):
        self.width = 9
        self.height = 20
        self.board = []
        self.left = 20
        self.top = -20
        self.cell_size = 40
        self.show_from = 6
        self.show_to = 19
        self.normal_lines_at_start = 7
        self.generate_board(self.height)

    def draw_board(self):
        for i in range(self.show_to - self.show_from):
            for j in range(self.width):
                y = self.top + i * self.cell_size
                self.board[i + self.show_from].draw_line(self.left, self.top + i * self.cell_size, self.cell_size)

    def generate_board(self):
        for i in range(self.normal_lines_at_start):
            self.board.append(Normal(...))
        for i in range(self.height - self.normal_lines_at_start):
            self.board.append(generate())

    def update_board(self):
        self.board.append(generate())
        self.board = self.board[1:]


class Line:
    def __init__(self, length):
        self.length = length
        self.line = []


    def draw_line(self, x, y, cell_size):
        for i in range(self.length):
            pass


class Normal:
    pass


class Car:
    def init(self, length):
        self.length = length
        self.line = []
        self.create_a_line()
        self.go_to_the_right = choice(True, False)

    def create_a_line(self):
        for i in range(self.length):
            self.line.append()



class River:
    pass


class Train:
    pass




if __name__ == "__main__":
    pygame.init()
    size = width, height = 400, 600
    screen = pygame.display.set_mode(size)

    running = True
    screen.fill((255, 255, 255))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(12):
                    for j in range(9):
                        pygame.draw.rect(screen, (0, 100, 150), ((20 + j * 40, 20 + i * 40), (40, 40)), 1)
        pygame.display.flip()

    pygame.quit()