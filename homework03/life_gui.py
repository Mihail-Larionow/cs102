import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.width = self.life.cols*cell_size
        self.height = self.life.rows*cell_size
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = self.width, self.height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed
        self.grid = self.life.create_grid(True)

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))
        pass

    def draw_grid(self) -> None:
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if self.grid[i][j] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('blue'),
                                     (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'),
                                     (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))
        pass

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        self.draw_lines()
        pygame.display.flip()
        running = True
        life = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    life = not(life)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]
                    x_cell = x // self.cell_size
                    y_cell = y // self.cell_size
                    if self.life.curr_generation[y_cell][x_cell] == 1:
                        self.life.curr_generation[y_cell][x_cell] = 0
                    else:
                        self.life.curr_generation[y_cell][x_cell] = 1
                    self.grid = self.life.curr_generation
                    self.draw_grid()
                    self.draw_lines()
                    pygame.display.flip()
            if life and self.life.is_changing and not(self.life.is_max_generations_exceeded):
                self.life.step()
                self.grid = self.life.curr_generation
                self.draw_grid()
                self.draw_lines()
                pygame.display.flip()
                clock.tick(self.speed)
        pygame.quit()
        pass



if __name__ == "__main__":
    game = GameOfLife(size=(120, 120))
    gui = GUI(game)
    gui.run()