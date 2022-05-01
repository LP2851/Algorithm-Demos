import time
import random

from gui import GUI
import pygame

pygame.font.init()

TILE_SIZE = 16
NO_OF_WALLS = 500

# COLORS
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

DEFAULT_TILE = (200, 200, 200)
WALL_TILE = (50, 50, 50)
VISITED_TILE = (50, 245, 250) # light blue


class PathfindingTile:
    """
    General pathfinding tile used to help with the animation
    """
    TILE = 0
    WALL = 1
    START_TILE = 2
    END_TILE = 3

    def __init__(self, pos: tuple[int, int], tag: int = TILE, default_color: tuple[int, int, int] = DEFAULT_TILE) -> None:
        """
        :param pos: Grid position of the tile
        :param tag: The tag that the tile has
        :param default_color: The color of the tile
        """
        self.color = default_color
        self.visited = False
        self.row, self.col = pos
        self.__rect = self.__generate_rect(self.row, self.col)
        self.tag = tag

    def is_start_tile(self) -> bool:
        """
        Returns if the tile is the start tile
        :return: True if the tile is the start tile
        :rtype: bool
        """
        return self.tag == self.START_TILE

    def is_end_tile(self) -> bool:
        """
        Returns if the tile is the end tile
        :return: True if the tile is the end tile
        :rtype: bool
        """
        return self.tag == self.END_TILE

    def is_wall(self) -> bool:
        """
        Returns if the tile is a wall tile
        :return: True if the tile is a wall tile
        :rtype: bool
        """
        return self.tag == self.WALL

    def set_wall(self) -> None:
        """
        Sets the tile to be a WALL tile and sets the color of the tile to the WALL_TILE color
        """
        self.tag = self.WALL
        self.color = WALL_TILE

    def set_start(self) -> None:
        """
        Sets the tile to a START_TILE
        """
        self.tag = self.START_TILE

    def set_end(self) -> None:
        """
        Sets the tile to an END_TILE
        """
        self.tag = self.END_TILE

    @staticmethod
    def __generate_rect(row, col) -> pygame.Rect:
        """
        Generates a rect object for the tile based on the tile's row and column values
        :param row: The row the tile is in
        :param col: The column the tile is in
        :return: A new rect object for a tile
        :rtype: pygame.Rect
        """
        return pygame.Rect(row * TILE_SIZE,
                           col * TILE_SIZE,
                           TILE_SIZE,
                           TILE_SIZE)

    def draw(self, window: pygame.Surface) -> None:
        """
        Redraws the tile on the window
        :param window: The window surface to be drawn onto
        """
        # Draw the tile
        pygame.draw.rect(window, self.color, self.__rect)

        # Adds start/end tile marker if necessary
        if self.tag == self.START_TILE:
            pygame.draw.circle(window,
                               GREEN,
                               (self.row * TILE_SIZE + (TILE_SIZE / 2), self.col * TILE_SIZE + (TILE_SIZE / 2)),
                               TILE_SIZE / 4)
        elif self.tag == self.END_TILE:
            pygame.draw.circle(window,
                               RED,
                               (self.row * TILE_SIZE + (TILE_SIZE / 2), self.col * TILE_SIZE + (TILE_SIZE / 2)),
                               TILE_SIZE / 4)

    def visit(self, color: tuple[int, int, int] = VISITED_TILE) -> None:
        """
        Marks the tile as visited and changes the color
        :param color:
        :return:
        """
        self.visited = True
        self.color = color


class ShowPathfindingGUI(GUI):
    """
    Generic class for a pathfinding GUI
    """
    def __init__(self, width: int, height: int, algo_name: str) -> None:
        """
        :param width: Width of the window
        :param height: Height of the window
        :param algo_name: Name of the algorithm being run
        """
        super().__init__(width, height)
        self._create_window(algo_name)
        self.map_tiles = []
        for row in range(width // TILE_SIZE):
            r = []
            for col in range(height // TILE_SIZE):
                r.append(PathfindingTile((row, col)))
            self.map_tiles.append(r)

        self._start_pos = (0, 0)
        self._end_pos = (0, 0)
        self.generate_map(NO_OF_WALLS)

    def start(self, wait_time: float) -> None:
        """
        Starts the pathfinding solver
        :param wait_time: The time to wait before starting the algorithm
        """
        time.sleep(wait_time)
        self.solve()

    def generate_map(self, max_walls: int) -> None:
        """
        Generates a random map for the pathfinder to run through
        :param max_walls: The maximum number of walls to generate
        """
        # Generates the walls for the map
        self.__generate_walls(max_walls)

        # Generates the starting position
        self._start_pos = self.generate_random_position(self._width, self._height)
        x, y = self._start_pos
        while self.map_tiles[x][y].is_wall(): # self.map_tiles[x][y]:
            self._start_pos = self.generate_random_position(self._width, self._height)
            x, y = self._start_pos
        self.map_tiles[x][y].set_start()

        # Generates the ending position
        self._end_pos = self.generate_random_position(self._width, self._height)
        x, y = self._end_pos
        while self.map_tiles[x][y].is_wall() or self.map_tiles[x][y].is_end_tile(): # self.map_tiles[x][y]:
            self._end_pos = self.generate_random_position(self._width, self._height)
            x, y = self._end_pos
        self.map_tiles[x][y].set_end()

    def __generate_walls(self, max_walls: int) -> None:
        """
        Generates a number of walls randomly on the map
        :param max_walls: The maximum number of walls to generate
        """
        for _ in range(max_walls):
            x, y = self.generate_random_position(self._width, self._height)
            # self.map_tiles[x][y] = True
            self.map_tiles[x][y].set_wall()

    @staticmethod
    def generate_random_position(width: int, height: int) -> tuple[int, int]:
        """
        Generates a random position tuple to be returned
        :param width: Width of the screen
        :param height: Height of the screen
        :return: Randomly generated position tuple
        :rtype: tuple[int, int]
        """
        x = random.randint(1, width // TILE_SIZE) - 1
        y = random.randint(1, height // TILE_SIZE) - 1
        return x, y

    def solve(self) -> None:
        """
        Method implemented by child classes
        """
        pass

    def draw(self) -> None:
        """
        Redraws the window
        """
        if self.check_events_exit():
            exit()

        self.window.fill((0, 0, 0))

        # Redrawing the tiles
        for row in range(len(self.map_tiles)):
            for col in range(len(self.map_tiles[0])):
                self.map_tiles[row][col].draw(self.window)

        # Draw grid lines
        for row in range(self._width // TILE_SIZE):
            pygame.draw.line(self.window, (0, 0, 0), (row * TILE_SIZE, 0), (row * TILE_SIZE, self._height), 1)
        for col in range(self._height // TILE_SIZE):
            pygame.draw.line(self.window, (0, 0, 0), (0, col * TILE_SIZE), (self._width, col * TILE_SIZE), 1)

        pygame.display.update()
        time.sleep(0.1)
