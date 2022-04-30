from __future__ import annotations
import time
import sys

from sorting import BubbleSort, MergeSort
from pathfinding import ShowPathfindingGUI


ELEMENTS_TO_SORT = 50


def arg_help() -> None:
    """
    Runs the --help command
    Prints all commands and their descriptions.
    """
    print("Help:")
    print("Here is a list of commands you can use.")
    for arg, val in all_args.items():
        print(f"\t{arg}: {val[0]}")
    input("Press enter to exit help menu.")


def arg_bubble_sort() -> None:
    """
    Runs the --bubble-sort command
    Runs and shows the user a bubble sort
    """
    sorter = BubbleSort(768, 512, ELEMENTS_TO_SORT)
    sorter.start(0.1)
    while not sorter.check_events_exit():
        pass
    sorter.close()


def arg_merge_sort() -> None:
    """
    Runs the --merge-sort command
    Runs and shows the user a merge sort
    """
    sorter = MergeSort(768, 512, ELEMENTS_TO_SORT)
    sorter.start(0.1)
    while not sorter.check_events_exit():
        pass
    sorter.close()


def arg_pathfinder() -> None:
    """
    Runs the --pathfinder command
    Runs a pathfinding algorithm (WIP)
    """
    pathfinder = ShowPathfindingGUI(768, 512, "test")
    pathfinder.draw()
    # while True:
    #     time.sleep(0.2)
    #     pathfinder.draw()

    # pathfinder.close()


def discard_arg(arg: str) -> None:
    """
    Tells the user that the arg found doesn't exist and has been discarded
    :param arg: The command that doesn't exist
    """
    # red, reset
    print(f"\u001b[31m[Command Error]: Discarded the command '{arg}'.\u001b[0m")


def check_args(args: list[str]) -> list[str]:
    """
    Checks all the args passed, removes invalid ones and returns the remaining ones
    :param args: All the arguments passed by the user
    :return: The list of arguments that are valid
    :rtype: list[str]
    """
    possible_args = []
    arg_keys = all_args.keys()

    for arg in args:
        # Making --help command run first
        if arg == "--help":
            possible_args = [arg] + possible_args
            continue
        if arg in arg_keys:
            possible_args.append(arg)
            continue
        discard_arg(arg)
    return possible_args


def run(args: list[str]) -> None:
    """
    Runs all commands in the order they were entered
    :param args: The valid arguments that will be run
    """
    for arg in args:
        # bold, green, reset, green, reset
        print(f"\u001b[1m\u001b[32mRunning:\u001b[0m\u001b[32m {arg}\u001b[0m")
        all_args[arg][1]()


def main(args: list[str]) -> None:
    """
    Checks all the arguments and then runs the valid ones
    :param args: All arguments from user
    """
    args = check_args(args)
    print()
    run(args)


# Dictionary containing for all commands: command -> [description, function]
all_args = {
    "--help": ["Prints the help menu.",
               arg_help],
    "--bubble-sort": ["SOMETHING",
                      arg_bubble_sort],
    "--pathfinder": ["",
                     arg_pathfinder],
    "--merge-sort": ["Performs a Merge Sort",
                     arg_merge_sort]
}

if __name__ == "__main__":
    argv = sys.argv[1:]
    main(argv)
