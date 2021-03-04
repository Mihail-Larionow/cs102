import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed
        self.grid = self.create_grid(True)

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()
            self.grid = self.get_next_generation()
            self.draw_grid()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = []
        for i in range(self.cell_height):
            row = []
            for j in range(self.cell_width):
                if randomize == False: x = 0
                else: x = random.randint(0, 1)
                row.append(x)
            grid.append(row)
        return grid

    def draw_grid(self) -> None:
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if self.grid[i][j] == 0:
                    pygame.draw.rect(self.screen, pygame.Color('white'), (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('blue'), (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))

    def get_neighbours(self, cell: Cell) -> Cells:
        cells = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    if cell[1] + j >= 0 and cell[0] + i >= 0:
                        if cell[1] + j < self.cell_width and cell[0] + i < self.cell_height:
                            cells.append(self.grid[cell[0] + i][cell[1] + j])
        return cells

    def get_next_generation(self) -> Grid:
        grid = []
        for i in range(self.cell_height):
            row = []
            for j in range(self.cell_width):
                cell = (i, j)
                neighbours = self.get_neighbours(cell)
                if (neighbours.count(1) == 2 or neighbours.count(1) == 3) and self.grid[i][j] == 1:
                    x = 1
                elif neighbours.count(1) == 3 and self.grid[i][j] == 0:
                    x = 1
                else:
                    x = 0
                row.append(x)
            grid.append(row)
        return grid


if __name__ == '__main__':
    game = GameOfLife(320, 240, 10)
    game.run()