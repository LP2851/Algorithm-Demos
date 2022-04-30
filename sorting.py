from __future__ import annotations
import pygame
import time
import random
from gui import GUI

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
    """
    SortingElement is a element that is being sorted
    """
    def __init__(self, value: float) -> None:
        """
        :param value: The value of the element
        """
        self.value = value
        self.focused = False

    @staticmethod
    def __is_sorting_element(other) -> bool:
        """
        Returns if the passed object is a sorting element
        :param other: The object to be checked
        :return: True if other is an instance of SortingElement
        :rtype: bool
        """
        return isinstance(other, SortingElement)

    def __ge__(self, other) -> bool:
        """
        >=
        :param other: B in `A >= B`
        :return: A >= B
        :rtype: bool
        """
        if not self.__is_sorting_element(other):
            raise TypeError
        return self.value >= other.value

    def __le__(self, other) -> bool:
        """
        <=
        :param other: B in `A <= B`
        :return: A <= B
        :rtype: bool
        """
        if not self.__is_sorting_element(other):
            raise TypeError
        return self.value <= other.value

    def __lt__(self, other) -> bool:
        """
        <
        :param other: B in `A < B`
        :return: A < B
        :rtype: bool
        """
        if not self.__is_sorting_element(other):
            raise TypeError
        return self.value < other.value

    def __gt__(self, other) -> bool:
        """
        >
        :param other: B in `A > B`
        :return: A > B
        :rtype: bool
        """
        if not self.__is_sorting_element(other):
            raise TypeError
        return self.value > other.value

    def __eq__(self, other) -> bool:
        """
        ==
        :param other: B in `A == B`
        :return: A == B
        :rtype: bool
        """
        if not self.__is_sorting_element(other):
            raise TypeError
        return self.value == other.value

    def __ne__(self, other) -> bool:
        """
        !=
        :param other: B in `A != B`
        :return: A != B
        :rtype: bool
        """
        if not self.__is_sorting_element(other):
            raise TypeError
        return self.value != other.value

    def __int__(self) -> int:
        """
        Integer value of this element
        :return: Value of this element as an int
        :rtype: int
        """
        return int(self.value)

    def __float__(self) -> float:
        """
        Float value of this element
        :return: Value of this element as a float
        :rtype: float
        """
        return float(self.value)

    def __repr__(self) -> str:
        """
        String representation of SortingElement
        :return: Representation of SortingElement
        :rtype: str
        """
        return str(self.value)


class ShowSortingGUI(GUI):
    """
    Generic class for a sorting algorithm GUI
    """
    def __init__(self, width: int, height: int, sort_name: str, frame_length: float = 0.1) -> None:
        """
        :param width: Width of the window
        :param height: Height of the window
        :param sort_name: Name of the sorting algorithm
        :param frame_length: Length of each frame
        """
        super().__init__(width, height)
        self._create_window(sort_name)
        self._to_sort = []
        self.complete = False
        self._frame_length = frame_length

    def start(self, wait_time: float) -> None:
        """
        Starts the sorting algorithm
        :param wait_time: Wait time before starting
        """
        time.sleep(wait_time)
        self.sort()

    def draw(self) -> None:
        """
        Redraws the window with the newest list
        :return:
        """
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
        """
        Sort function: implemented in child classes
        """
        pass

    def generate_values_to_sort(self, amount: int) -> list[SortingElement]:
        """
        Generates the list of values being sorted
        :param amount: Length of list requested
        :return: Randomly generated list of SortingElements
        :rtype: list[SortingElement]
        """
        max_height = self._height * 0.9
        out = []
        for _ in range(amount):
            out.append(SortingElement(random.random() * max_height))
        return out


class BubbleSort(ShowSortingGUI):
    """
    Runs and displays a Bubble Sort
    """
    def __init__(self, width: int, height: int, elements: int) -> None:
        """
        :param width: Width of the window
        :param height: Height of the window
        :param elements: Number of elements to sort
        """
        super().__init__(width, height, "Bubble Sort")
        self._to_sort = self.generate_values_to_sort(elements)
        self.draw()

    def sort(self) -> None:
        """
        Runs the Bubble Sort algorithm
        """
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
