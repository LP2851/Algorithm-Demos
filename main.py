from __future__ import annotations
import time
import sys

from sorting import BubbleSort
from pathfinding import ShowPathfindingGUI


ELEMENTS_TO_SORT = 50


def arg_help() -> None:
    print("Help:")
    print("Here is a list of commands you can use.")
    for arg, val in all_args.items():
        print(f"\t{arg}: {val[0]}")
    input("Press enter to exit help menu.")


def arg_bubble_sort() -> None:
    sorter = BubbleSort(768, 512, ELEMENTS_TO_SORT)
    sorter.start(0.1)
    while not sorter.check_events_exit():
        pass
    sorter.close()


def arg_pathfinder() -> None:
    pathfinder = ShowPathfindingGUI(768, 512, "test")
    pathfinder.draw()
    # while True:
    #     time.sleep(0.2)
    #     pathfinder.draw()

    # pathfinder.close()


def discard_arg(arg: str) -> None:
    # red, reset
    print(f"\u001b[31m[Command Error]: Discarded the command '{arg}'.\u001b[0m")


def check_args(args: list[str]) -> list[str]:
    possible_args = []
    arg_keys = all_args.keys()

    for arg in args:
        if arg == "--help":
            possible_args = [arg] + possible_args
            continue
        if arg in arg_keys:
            possible_args.append(arg)
            continue
        discard_arg(arg)
    return possible_args


def run(args: list[str]) -> None:
    for arg in args:
        # bold, green, reset, green, reset
        print(f"\u001b[1m\u001b[32mRunning:\u001b[0m\u001b[32m {arg}\u001b[0m")
        all_args[arg][1]()


def main(args: list[str]) -> None:
    args = check_args(args)
    print()
    run(args)


all_args = {
    "--help": ["Prints the help menu.",
               arg_help],
    "--bubble-sort": ["SOMETHING",
                      arg_bubble_sort],
    "--pathfinder": ["",
                     arg_pathfinder]
}

if __name__ == "__main__":
    argv = sys.argv[1:]
    main(argv)
