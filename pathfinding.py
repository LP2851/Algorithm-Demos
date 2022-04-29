import time
import random

from gui import GUI
import pygame
pygame.font.init()

TILE_SIZE = 16


class ShowPathfindingGUI(GUI):
    def __init__(self, width: int, height: int, algo_name: str) -> None:
        super().__init__(width, height)
        self._create_window(algo_name)
        self.map_tiles = []
        for _ in range(width // TILE_SIZE):
            row = []
            for _ in range(height // TILE_SIZE):
                row.append(False)
            self.map_tiles.append(row)

        self._start_pos = (0, 0)
        self._end_pos = (0, 0)
        self.generate_map(500)

    def start(self, wait_time: float) -> None:
        time.sleep(wait_time)
        self.solve()

    def generate_map(self, no_walls: int) -> None:
        self.__generate_walls(no_walls)
        self._start_pos = self.generate_random_position(self._width, self._height)
        x, y = self._start_pos
        while self.map_tiles[x][y]:
            self._start_pos = self.generate_random_position(self._width, self._height)

        self._end_pos = self.generate_random_position(self._width, self._height)
        x, y = self._end_pos
        while self.map_tiles[x][y]:
            self._end_pos = self.generate_random_position(self._width, self._height)

    def __generate_walls(self, no_walls: int) -> None:
        for _ in range(no_walls):
            x, y = self.generate_random_position(self._width, self._height)
            self.map_tiles[x][y] = True

    @staticmethod
    def generate_random_position(width: int, height: int) -> tuple[int, int]:
        x = random.randint(1, width // TILE_SIZE) - 1
        y = random.randint(1, height // TILE_SIZE) - 1
        return x, y

    def solve(self) -> None:
        pass

    def draw(self) -> None:
        if self.check_events_exit():
            exit()
        self.window.fill((0, 0, 0))

        for row in range(self._width // TILE_SIZE):
            for col in range(self._height // TILE_SIZE):
                rect = pygame.Rect(row * TILE_SIZE,
                                   col * TILE_SIZE,
                                   TILE_SIZE,
                                   TILE_SIZE)

                color = (50, 50, 50) if self.map_tiles[row][col] else (200, 200, 200)
                pygame.draw.rect(self.window, color, rect)
                if (row, col) == self._start_pos:
                    pygame.draw.circle(self.window,
                                       (0, 255, 0),
                                       (row * TILE_SIZE + (TILE_SIZE / 2), col * TILE_SIZE + (TILE_SIZE / 2)),
                                       TILE_SIZE / 4)
                elif (row, col) == self._end_pos:
                    pygame.draw.circle(self.window,
                                       (255, 0, 0),
                                       (row * TILE_SIZE + (TILE_SIZE / 2), col * TILE_SIZE + (TILE_SIZE / 2)),
                                       TILE_SIZE / 4)

        # Draw grid lines
        for row in range(self._width // TILE_SIZE):
            pygame.draw.line(self.window, (0, 0, 0), (row * TILE_SIZE, 0), (row * TILE_SIZE, self._height), 1)
        for col in range(self._height // TILE_SIZE):
            pygame.draw.line(self.window, (0, 0, 0), (0, col * TILE_SIZE), (self._width, col * TILE_SIZE), 1)

        pygame.display.update()
        time.sleep(0.1)
