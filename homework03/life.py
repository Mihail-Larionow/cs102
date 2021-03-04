import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                if randomize:
                    x = random.randint(0, 1)
                else:
                    x = 0
                row.append(x)
            grid.append(row)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        cells = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != 0 or j != 0:
                    if cell[1] + j >= 0 and cell[0] + i >= 0:
                        if cell[1] + j < self.cols and cell[0] + i < self.rows:
                            cells.append(self.curr_generation[cell[0] + i][cell[1] + j])
        return cells

    def get_next_generation(self) -> Grid:
        grid = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                cell = (i, j)
                neighbours = self.get_neighbours(cell)
                if (neighbours.count(1) == 2 or neighbours.count(1) == 3) and self.curr_generation[i][j] == 1:
                    x = 1
                elif neighbours.count(1) == 3 and self.curr_generation[i][j] == 0:
                    x = 1
                else:
                    x = 0
                row.append(x)
            grid.append(row)
        return grid

    def step(self) -> None:
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        for i in range(len(self.prev_generation)):
            for j in range(len(self.prev_generation[0])):
                if self.curr_generation[i][j] != self.prev_generation[i][j]:
                    return True
        return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        with open(filename, 'r') as file:
            data = json.load(file)
            lg = GameOfLife(
                size=(data["rows"], data["cols"]),
                randomize=data["randomize"],
                max_generations=data["max_generations"],
            )
            lg.generations = ob["generations"]
            lg.prev_generation = ob["prev_generation"]
            lg.curr_generation = ob["curr_generation"]
            return lg

    def save(self, filename: pathlib.Path) -> None:
        data = {
            "rows": self.rows,
            "cols": self.cols,
            "randomize": self.randomize,
            "generations": self.generations,
            "prev_generation": self.prev_generation,
            "curr_generation": self.curr_generation,
            "max_generations": self.max_generations,
        }
        with open(filename, 'w') as file:
            json.dump(data, file)

