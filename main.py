from __future__ import annotations
import time
import sys

from sorting import BubbleSort, MergeSort, QuickSort
from simplesearches import DepthFirstSearch, BreadthFirstSearch
from pathfinders import DijkstraAlgoSearch, AStarSearch

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


def arg_all() -> None:
    for arg, [_, func] in all_args.items():
        if arg == "--help" or arg == "--all":
            continue
        # bold, green, reset, green, reset
        print(f"\u001b[1m\u001b[32mRunning:\u001b[0m\u001b[32m {arg}\u001b[0m")
        func()


def arg_bubble_sort() -> None:
    """
    Runs the --bubble-sort command
    Runs and shows the user a bubble sort
    """
    sorter = BubbleSort(768, 512, ELEMENTS_TO_SORT // 5)
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


def arg_quick_sort() -> None:
    """
    Runs the --quick-sort command
    Runs and shows the user a quick sort
    """
    sorter = QuickSort(768, 512, ELEMENTS_TO_SORT)
    sorter.start(0.1)
    while not sorter.check_events_exit():
        pass
    sorter.close()


def arg_dfs() -> None:
    """
    Runs the --dfs command
    """
    pathfinder = DepthFirstSearch(768, 512)
    pathfinder.draw()
    pathfinder.start(0.1)
    while not pathfinder.check_events_exit():
        pass

    pathfinder.close()


def arg_bfs() -> None:
    """
    Runs the --bfs command
    """
    pathfinder = BreadthFirstSearch(768, 512)
    pathfinder.draw()
    pathfinder.start(0.1)
    while not pathfinder.check_events_exit():
        pass

    pathfinder.close()


def arg_dijkstra_algo() -> None:
    """
    Runs the --dijkstra-algo command
    """
    pathfinder = DijkstraAlgoSearch(768, 512)
    pathfinder.draw()
    pathfinder.start(0.1)
    while not pathfinder.check_events_exit():
        pass

    pathfinder.close()


def arg_a_star_algo() -> None:
    """
    Runs the --a-star command
    """
    pathfinder = AStarSearch(768, 512)
    pathfinder.draw()
    pathfinder.start(0.1)
    while not pathfinder.check_events_exit():
        pass

    pathfinder.close()


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


def get_manual_input_args() -> list[str]:
    """
    Manually gets the arguments from the user if none were entered.
    :return: The list of arguments the user entered
    :rtype: list[str]
    """
    # Red
    print("\u001b[31m")
    print(f"[Command Error]: You have not run this program with any commands.")
    arg_help()
    print("Type a list of arguments you would like to run in the form: '--bfs --quick-sort'")
    # End red
    print("\u001b[0m")

    arg_str = input("Please enter arguments here: ")
    return arg_str.split(" ")


def main(args: list[str]) -> None:
    """
    Checks all the arguments and then runs the valid ones
    :param args: All arguments from user
    """

    # Manually gets the arguments from the user if none were entered.
    if len(args) == 0:
        args = get_manual_input_args()

    args = check_args(args)
    print()
    run(args)


# Dictionary containing for all commands: command -> [description, function]
all_args = {
    "--help": ["Prints the help menu.",
               arg_help],
    "--all" : ["Runs all of the command in order (apart from '--help').",
               arg_all],
    "--bubble-sort": ["Performs a Bubble Sort",
                      arg_bubble_sort],
    "--merge-sort": ["Performs a Merge Sort",
                     arg_merge_sort],
    "--quick-sort": ["Performs a Quick Sort",
                     arg_quick_sort],
    "--dfs": ["Performs a DFS",
              arg_dfs],
    "--bfs": ["Performs a BFS",
              arg_bfs],
    "--dijkstra-algo": ["Performs Dijkstra's Algorithm to find shortest path",
                        arg_dijkstra_algo],
    "--a-star": ["Performs A* Search to find shortest path",
                      arg_a_star_algo],
}


if __name__ == "__main__":
    argv = sys.argv[1:]
    main(argv)
