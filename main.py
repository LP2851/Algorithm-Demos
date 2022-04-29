import time

from sorting import BubbleSort
from pathfinding import ShowPathfindingGUI


def main():
    # sorter = BubbleSort(768, 512, 50)
    # sorter.start(0.1)
    # while not sorter.check_events_exit():
    #     pass
    pathfinder = ShowPathfindingGUI(768, 512, "test")
    pathfinder.draw()
    while True:
        time.sleep(0.2)
        pathfinder.draw()


if __name__ == "__main__":
    main()