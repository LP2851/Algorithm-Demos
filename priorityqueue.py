from __future__ import annotations


class PriorityQueue:
    """
    Priority Queue class
    Elements of the queue are given a priority with which they are served.
    """
    def __init__(self, low_priority_first: bool = True) -> None:
        """
        Creates a new PriorityQueue
        :param low_priority_first: If low priority is served first
        """
        self.__low_priority_first = low_priority_first
        self.elements = []

    def empty(self) -> bool:
        """
        Returns if the queue is empty or not
        :return: True if the queue is empty, otherwise false
        :rtype: bool
        """
        return not self.elements

    def enqueue(self, item, priority: float) -> PriorityQueue:
        """
        Enqueues (adds to queue) the item with its priority
        :param item: The item to be added to the queue
        :param priority: The priority of the item
        :return: This priority queue
        :rtype: PriorityQueue
        """
        self.elements.append((item, priority))
        return self

    def dequeue(self):
        """
        Returns the next item in the queue based on the priority
        :return: The next item in the queue
        """
        # I know this isn't the best implementation
        self.elements = sorted(self.elements, key=lambda x: x[1], reverse=not self.__low_priority_first)
        return self.elements.pop(0)[0]
