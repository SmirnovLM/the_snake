"""
Игровая программа 'Змейка'.

Этот модуль реализует классическую игру "Змейка" с использованием Pygame.
"""
import os
from random import choice, randint

import pygame

# Файл для записи результата:
RECORD_FILE = 'record.txt'

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 15

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Описание основных классов:
class GameObject:
    """Это базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self, position=(0, 0), body_color=(255, 255, 255)):
        """Инициализация базового игрового объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """
        Метод для отрисовки объекта на экране.

        Этот метод должен быть переопределен в дочерних классах.
        """
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко."""

    def __init__(self):
        """Инициализация."""
        super().__init__((0, 0), APPLE_COLOR)
        self.randomize_position()

    def randomize_position(self):
        """Генерация случайной позиции яблока."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Отрисовка яблока на экране."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку."""

    def __init__(self):
        """Инициализация."""
        center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        super().__init__(center, SNAKE_COLOR)
        self.positions = [center]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет положение змейки."""
        head_x, head_y = self.get_head_position()
        new_head = (
            (head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )

        if new_head in self.positions[1:]:
            self.reset()
            return

        self.positions.insert(0, new_head)
        self.last = None
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Отрисовка змейки на экране."""
        for pos in self.positions:
            rect = pygame.Rect(pos, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.positions = [center]
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(snake):
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
            elif event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def read_record():
    """Считывает рекорд из файла."""
    if os.path.exists(RECORD_FILE):
        with open(RECORD_FILE, 'r') as file:
            try:
                return int(file.read().strip())
            except ValueError:
                pass
    return 1


def save_record(record):
    """Сохраняет рекорд в файл."""
    with open(RECORD_FILE, 'w') as file:
        file.write(str(record))


def main():
    """Основной цикл игры."""
    snake = Snake()
    apple = Apple()
    record_length = read_record()
    pygame.display.set_caption(f'Змейка | Рекорд: {record_length}')

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

            if snake.length > record_length:
                record_length = snake.length
                save_record(record_length)
                pygame.display.set_caption(f'Змейка | Рекорд: {record_length}')

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
