import random

import pygame

pygame.init()

CELL_SIZE = 50
SCREEN_WIDTH = CELL_SIZE * 9
SCREEN_HEIGHT = CELL_SIZE * 16
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CrossyRoad")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (252, 190, 187)  # Локация отдыха

# Игровые объекты
player = pygame.Rect((SCREEN_WIDTH // 2) - (CELL_SIZE // 2), SCREEN_HEIGHT - CELL_SIZE, CELL_SIZE, CELL_SIZE)
stones = []
game_over = False
game_started = False
start_time = 0
background_y = 0


# Класс кнопки
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)
        text_surface = pygame.font.SysFont(None, 36).render(self.text, True, WHITE)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# Функция генерации локации отдыха
def generate_rest_location():
    global stones
    stones.clear()
    attempts = 0
    while len(stones) < random.randint(20, 30) and attempts < 100:
        x = random.randint(0, 8) * CELL_SIZE
        y = random.randint(0, 15) * CELL_SIZE

        if not is_adjacent_to_stone(x, y) and (
                x != SCREEN_WIDTH // 2 - CELL_SIZE // 2 or y != SCREEN_HEIGHT - CELL_SIZE):
            stones.append(pygame.Rect(x, y, CELL_SIZE, CELL_SIZE))
        attempts += 1


# Функция проверки соседних клеток
def is_adjacent_to_stone(x, y):
    for stone in stones:
        for dx in [-CELL_SIZE, 0, CELL_SIZE]:
            for dy in [-CELL_SIZE, 0, CELL_SIZE]:
                if dx == 0 and dy == 0:
                    continue
                if stone.collidepoint(x + dx, y + dy):
                    return True
    return False


# Функция проверки допустимости движения
def is_move_valid(dx, dy):
    new_position = player.move(dx, dy)

    # Столкновение с камнями
    for stone in stones:
        if new_position.colliderect(stone):
            return False

    # Проверка, не выходит ли игрок за границы
    if new_position.left < 0 or new_position.right > SCREEN_WIDTH:
        return False

    return True


# Отображение игры
def draw_game():
    screen.fill(WHITE)

    pygame.draw.rect(screen, PINK, (0, background_y, SCREEN_WIDTH, SCREEN_HEIGHT))

    # Сетка
    for y in range(16):
        for x in range(9):
            pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    # Камни
    for stone in stones:
        pygame.draw.rect(screen, RED, stone)

    # Игрок
    pygame.draw.rect(screen, GREEN, player)

    if game_over:
        screen.fill(WHITE)
        game_over_text = pygame.font.SysFont(None, 72).render("Игра окончена!", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
        restart_button.draw(screen)

    pygame.display.update()


# Обработчик событий
def handle_events():
    global game_over, player, restart_button, game_started, start_time
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            if restart_button.is_clicked(event.pos):
                reset_game()

        if event.type == pygame.KEYDOWN and not game_over:
            if not game_started:
                game_started = True
                start_time = pygame.time.get_ticks()

            # Движение игрока
            if event.key == pygame.K_LEFT:
                dx, dy = -CELL_SIZE, 0
            elif event.key == pygame.K_RIGHT:
                dx, dy = CELL_SIZE, 0
            elif event.key == pygame.K_UP:
                dx, dy = 0, -CELL_SIZE
            elif event.key == pygame.K_DOWN:
                dx, dy = 0, CELL_SIZE
            else:
                continue

            if is_move_valid(dx, dy):
                player.x += dx
                player.y += dy

            if player.y >= SCREEN_HEIGHT:
                game_over = True

    return True


# Обновление положения объектов
def update_objects():
    global start_time, background_y
    if game_started and not game_over:
        current_time = pygame.time.get_ticks()
        if current_time - start_time >= 1000:
            start_time = current_time

            # Перемещение объектов вниз
            for stone in stones:
                stone.y += CELL_SIZE
            if player.y + CELL_SIZE < SCREEN_HEIGHT:
                player.y += CELL_SIZE

            background_y += CELL_SIZE

            stones[:] = [stone for stone in stones if stone.top < SCREEN_HEIGHT]


# Сброс игры
def reset_game():
    global game_over, player, game_started, background_y
    game_over = False
    game_started = False
    background_y = 0
    player = pygame.Rect((SCREEN_WIDTH // 2) - (CELL_SIZE // 2), SCREEN_HEIGHT - CELL_SIZE, CELL_SIZE, CELL_SIZE)
    generate_rest_location()


# Главная функция
def main():
    global restart_button

    restart_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50, "Начать заново")
    generate_rest_location()
    clock = pygame.time.Clock()

    running = True
    while running:
        running = handle_events()
        update_objects()
        draw_game()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
