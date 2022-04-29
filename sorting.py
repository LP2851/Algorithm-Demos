import pygame
import time
import random
from gui import GUI
from dataclasses import dataclass
pygame.font.init()

WIDTH = 768
HEIGHT = 512

SPACE_BETWEEN_BARS = 5

FRAME_LENGTH = 0.1

# COLORS
BLACK   = (  0,   0,   0)
WHITE   = (255, 255, 255)
RED     = (255,   0,   0)
GREEN   = (  0, 255,   0)
BLUE    = (  0,   0, 255)


class ShowSortingGUI(GUI):
    def __init__(self, width: int, height: int, sort_name: str) -> None:
        super().__init__(width, height)
        self._create_window(sort_name)
        self._to_sort = []
        self.focused_indexes = []
        self.complete = False

    def start(self, wait_time: float) -> None:
        time.sleep(wait_time)
        self.sort()

    def draw(self) -> None:
        if self.check_events_exit():
            exit()

        # Making the window black
        self.window.fill(BLACK)
        length = len(self._to_sort)

        bar_width = (self._width - (SPACE_BETWEEN_BARS * (length + 1))) / length

        for i, val in enumerate(self._to_sort):
            # LEFT, TOP, WIDTH, HEIGHT
            rect = pygame.Rect((i+1) * SPACE_BETWEEN_BARS + i * bar_width,
                               self._height - val,
                               bar_width,
                               val)
            if self.complete:
                color = GREEN
            else:
                color = GREEN if i in self.focused_indexes else WHITE

            pygame.draw.rect(self.window, color, rect)

        self.focused_indexes.clear()
        pygame.display.update()
        time.sleep(FRAME_LENGTH)

    def sort(self) -> None:
        pass

    def generate_values_to_sort(self, amount: int) -> list[float]:
        max_height = self._height * 0.9
        out = []
        for _ in range(amount):
            out.append(random.random() * max_height)
        return out


class BubbleSort(ShowSortingGUI):
    def __init__(self, width: int, height: int, elements: int) -> None:
        super().__init__(width, height, "Bubble Sort")
        self._to_sort = self.generate_values_to_sort(elements)
        self.draw()

    def sort(self) -> None:
        changed = True

        while changed:
            changed = False
            for i in range(len(self._to_sort)-1):
                self.focused_indexes.append(i)
                self.focused_indexes.append(i+1)
                if self._to_sort[i] > self._to_sort[i+1]:
                    self._to_sort[i], self._to_sort[i+1] = self._to_sort[i+1], self._to_sort[i]
                    changed = True
                self.draw()

        self.complete = True
        self.draw()

