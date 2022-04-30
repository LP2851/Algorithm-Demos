from __future__ import annotations
import pygame
import time
import random
from gui import GUI
from dataclasses import dataclass
pygame.font.init()

WIDTH = 768
HEIGHT = 512

SPACE_BETWEEN_BARS = 5

# COLORS
BLACK   = (  0,   0,   0)
WHITE   = (255, 255, 255)
RED     = (255,   0,   0)
GREEN   = (  0, 255,   0)
BLUE    = (  0,   0, 255)


class SortingElement:
    def __init__(self, value: float) -> None:
        self.value = value
        self.focused = False

    @staticmethod
    def __other_is_sorting_element(other) -> bool:
        return isinstance(other, SortingElement)

    def __ge__(self, other):
        if not self.__other_is_sorting_element(other):
            raise TypeError
        return self.value >= other.value

    def __le__(self, other):
        if not self.__other_is_sorting_element(other):
            raise TypeError
        return self.value <= other.value

    def __lt__(self, other):
        if not self.__other_is_sorting_element(other):
            raise TypeError
        return self.value < other.value

    def __gt__(self, other):
        if not self.__other_is_sorting_element(other):
            raise TypeError
        return self.value > other.value

    def __eq__(self, other):
        if not self.__other_is_sorting_element(other):
            raise TypeError
        return self.value == other.value

    def __ne__(self, other):
        if not self.__other_is_sorting_element(other):
            raise TypeError
        return self.value != other.value

    def __int__(self):
        return self.value

    def __float__(self):
        return self.value

    def __repr__(self):
        return str(self.value)


class ShowSortingGUI(GUI):
    def __init__(self, width: int, height: int, sort_name: str, frame_length: float = 0.1) -> None:
        super().__init__(width, height)
        self._create_window(sort_name)
        self._to_sort = []
        self.complete = False
        self._frame_length = frame_length

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
                               self._height - val.value,
                               bar_width,
                               val.value)
            if self.complete:
                color = GREEN
            else:
                color = GREEN if val.focused else WHITE
                val.focused = False

            pygame.draw.rect(self.window, color, rect)

        pygame.display.update()
        time.sleep(self._frame_length)

    def sort(self) -> None:
        pass

    def generate_values_to_sort(self, amount: int) -> list[SortingElement]:
        max_height = self._height * 0.9
        out = []
        for _ in range(amount):
            out.append(SortingElement(random.random() * max_height))
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
                self._to_sort[i].focused = True
                self._to_sort[i + 1].focused = True
                if self._to_sort[i] > self._to_sort[i+1]:
                    self._to_sort[i], self._to_sort[i+1] = self._to_sort[i+1], self._to_sort[i]
                    changed = True
                self.draw()

        self.complete = True
        self.draw()


class MergeSort(ShowSortingGUI):
    def __init__(self, width: int, height: int, elements: int) -> None:
        super().__init__(width, height, "Merge Sort", frame_length=0.02)
        self._to_sort = self.generate_values_to_sort(elements)
        self.draw()

    def __merge(self, start: int, middle: int, end: int) -> None:
        left = self._to_sort[start:middle+1]
        right = self._to_sort[middle+1:end+1]

        i = j = 0
        k = start

        while i < len(left) and j < len(right):
            left[i].focused = True
            right[j].focused = True
            self.draw()
            left[i].focused = True
            right[j].focused = True
            if left[i] < right[j]:
                print(f"{left[i]}<{right[j]}")
                self._to_sort[k] = left[i]
                i += 1
            else:
                self._to_sort[k] = right[j]
                j += 1
            k += 1
            self.draw()

        while i < len(left):
            left[i].focused = True
            self.draw()
            left[i].focused = True
            self._to_sort[k] = left[i]
            i += 1
            k += 1
            self.draw()

        while j < len(right):
            right[j].focused = True
            self.draw()
            right[j].focused = True
            self._to_sort[k] = right[j]
            j += 1
            k += 1
            self.draw()

    def __merge_sort(self, start: int, end: int) -> None:
        if start < end:
            mid = int((start + end) / 2)
            self.__merge_sort(start, mid)
            self.__merge_sort(mid+1, end)

            self.__merge(start, mid, end)

    def sort(self) -> None:
        self.__merge_sort(0, len(self._to_sort)-1)
        self.complete = True
        self.draw()
