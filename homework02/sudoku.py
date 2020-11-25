from typing import Tuple, List, Set, Optional
from math import *
import copy
import random

def read_sudoku(filename: str) -> List[List[str]]:
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(grid: List[List[str]]) -> None:
    """Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(grid[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def group(values: List[str], n: int) -> List[List[str]]:
    """ Сгруппировать значения values в список, состоящий из списков по n элементов """
    main_group = []
    digit = 0
    while digit < len(values):
        small_group = values[digit : digit + n]
        main_group.append(small_group)
        digit = digit + n
    return main_group


def get_row(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """" Возвращает все значения для номера строки, указанной в pos """
    return grid[pos[0]]


def get_col(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения для номера столбца, указанного в pos """
    col = []
    for row in grid:
        col.append(row[pos[1]])
    return col


def get_block(grid: List[List[str]], pos: Tuple[int, int]) -> List[str]:
    """ Возвращает все значения из квадрата, в который попадает позиция pos """
    block = []
    summary_block = int(sqrt(len(grid)))
    row = int(pos[0]/summary_block)
    col = int(pos[1] / summary_block)
    for i_row in range(summary_block):
        for j_col in range(summary_block):
            block.append(grid[row*summary_block + i_row][col*summary_block+j_col])
    return block


def find_empty_positions(grid: List[List[str]]) -> Optional[Tuple[int, int]]:
    """ Найти первую свободную позицию в пазле"""
    for i_row in grid:
        for j_col in i_row:
            if j_col == ".":
                return (grid.index(i_row), i_row.index(j_col))
    return (-1, -1)


def find_possible_values(grid: List[List[str]], pos: Tuple[int, int]) -> Set[str]:
    """ Вернуть множество возможных значения для указанной позиции """
    values = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}
    possible_values = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}
    row = get_row(grid, pos)
    col = get_col(grid, pos)
    block = get_block(grid, pos)
    for value in values:
        if value in row or value in col or value in block:
            possible_values.remove(value)
    return possible_values


def solve(grid: List[List[str]]) -> Optional[List[List[str]]]:
    pos = find_empty_positions(grid)
    if pos[0] != -1:
        possible_values = find_possible_values(grid, pos)
        for value in possible_values:
            grid_sol = copy.deepcopy(grid)
            grid_sol[pos[0]][pos[1]] = value
            solution = solve(grid_sol)
            if find_empty_positions(solution)[0] == -1: return solution
    return grid


def check_solution(solution: List[List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False """
    if find_empty_positions(solution)[0] == -1:
        for i_row in range(len(solution)):
            for j_col in range(len(solution)):
                pos = (i_row, j_col)
                if len(set(get_row(solution, pos))) != len(solution): return False
                if len(set(get_col(solution, pos))) != len(solution): return False
                if len(set(get_block(solution, pos))) != len(solution): return False
        return True
    return False


def generate_sudoku(N: int) -> List[List[str]]:
    """ Генерация судоку заполненного на N элементов """
    if N>81: N=81
    blank = []

    for temp in range(81):
        blank.append(".")
    grid = group(blank, 9)
    positions = []
    for i_row in range(9):
        for j_col in range(9):
            positions.append((i_row, j_col))
    for temp in range(N):
        pos = random.choice(positions)
        possible_values = find_possible_values(grid, pos)
        if possible_values:
            grid[pos[0]][pos[1]] = list(possible_values)[0]
            positions.remove(pos)
    while not check_solution(solve(grid)):
        grid = group(blank, 9)
        positions = []
        for i_row in range(9):
            for j_col in range(9):
                positions.append((i_row, j_col))
        for temp in range(N):
            pos = random.choice(positions)
            possible_values = find_possible_values(grid, pos)
            if possible_values:
                grid[pos[0]][pos[1]] = list(possible_values)[0]
                positions.remove(pos)
    return grid


if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
