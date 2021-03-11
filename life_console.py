import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife, speed: int = 1) -> None:
        super().__init__(life)
        self.speed = speed
        self.grid = self.life.create_grid(True)

    def draw_borders(self, screen) -> None:
        curses.resizeterm(self.life.rows+2, self.life.cols+2)
        screen.border()
        pass

    def draw_grid(self, screen) -> None:
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.grid[i][j] == 1: screen.addstr(i+1, j+1, '*')
                else: screen.addstr(i+1, j+1, ' ')
        pass

    def run(self) -> None:
        screen = curses.initscr()
        self.draw_borders(screen)
        screen.refresh()
        running = True
        life = True
        while running:
            if life and self.life.is_changing and not (self.life.is_max_generations_exceeded):
                self.life.step()
                self.grid = self.life.curr_generation
                self.draw_borders(screen)
                self.draw_grid(screen)
                screen.refresh()
                time.sleep(self.speed)
        curses.endwin()


if __name__ == "__main__":
    game = GameOfLife(size=(10, 30), max_generations=10)
    console = Console(game)
    curses.update_lines_cols()
    curses.wrapper(console.run())