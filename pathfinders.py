from __future__ import annotations

import math
import priorityqueue

from simplesearches import ShowPathfindingGUI, PathfindingTile

# Large value (like an infinity value)
LARGE_VALUE = 1000000


class DijkstraAlgoSearch(ShowPathfindingGUI):
    """
    Runs a visualisation of Dijkstra's Algorithm
    """
    def __init__(self, width: int, height: int) -> None:
        """
        :param width: Width of the window
        :param height: Height of the window
        """
        super().__init__(width, height, "Dijkstra's Algorithm", frame_time=0)
        self.draw()
        self.graph_flat = DijkstraAlgoSearch.flatten_tiles_map(self.map_tiles)

    def __dijkstra_algorithm(self, start_node: PathfindingTile) \
            -> tuple[dict[PathfindingTile, PathfindingTile], dict[PathfindingTile, int]]:
        """
        Runs dijkstra's algorithm on the graph/grid of tiles
        :param start_node: The node act as the start node
        :return: Dictionary for the previous nodes and dictionary for shortest path values
        :rtype: tuple[dict[PathfindingTile, PathfindingTile], dict[PathfindingTile, int]]
        """
        # List of all nodes
        unvisited_nodes = self.graph_flat.copy()
        # Best-known cost to all nodes
        shortest_path = {}

        prev_nodes = {}

        for node in unvisited_nodes:
            shortest_path[node] = LARGE_VALUE
        shortest_path[start_node] = 0

        while unvisited_nodes:
            current_node = None

            for node in unvisited_nodes:
                if not current_node:
                    current_node = node
                elif shortest_path[node] < shortest_path[current_node]:
                    current_node = node

            # Skipping all wall nodes
            if current_node.is_wall():
                unvisited_nodes.remove(current_node)
                continue

            neighbours = current_node.neighbours
            for neighbour in neighbours:
                # All tile distances are worth 1 distance point, hence + 1
                distance = shortest_path[current_node] + 1
                if distance < shortest_path[neighbour]:
                    shortest_path[neighbour] = distance
                    prev_nodes[neighbour] = current_node

            current_node.visit()
            self.draw()
            unvisited_nodes.remove(current_node)
        return prev_nodes, shortest_path

    def display_path_from_prev_nodes(self, prev_nodes: dict[PathfindingTile, PathfindingTile]) -> None:
        """
        Displays the path using the prev_nodes that were found using Dijkstra's Algorithm
        :param prev_nodes: Dictionary linking nodes to previous nodes representing paths to the starting node
        """
        x, y = self._start_pos
        start_node = self.map_tiles[x][y]
        x, y = self._end_pos
        end_node = self.map_tiles[x][y]

        current_node = end_node

        start_node.color = (7, 138, 0)

        while current_node != start_node:
            # GREEN
            current_node.color = (7, 138, 0)
            current_node = prev_nodes[current_node]
            self.draw()

    def solve(self) -> None:
        """
        Runs Dijkstra's Algorithm and displays the results to the user
        """
        x, y = self._start_pos
        start_node = self.map_tiles[x][y]
        # Solve
        prev_nodes, _ = self.__dijkstra_algorithm(start_node)
        self._frame_time = 0.05
        # Display path
        self.display_path_from_prev_nodes(prev_nodes)
        self.complete = True


class AStarSearch(ShowPathfindingGUI):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height, "A* Search Algorithm", frame_time=0.1)
        self.draw()
        self.graph_flat = DijkstraAlgoSearch.flatten_tiles_map(self.map_tiles)

    @staticmethod
    def __calculate_heuristic(node_a: PathfindingTile, node_b: PathfindingTile) -> float:
        ax, ay = node_a.get_pos()
        bx, by = node_b.get_pos()
        # Pythagoras
        return math.sqrt((ax - bx) ** 2 + abs(ay - by) ** 2)

    def __a_star(self, start_node: PathfindingTile, end_node: PathfindingTile) \
            -> tuple[dict[PathfindingTile, PathfindingTile], dict[PathfindingTile, int]]:
        # g: Distance between current node and start node
        # h: Heuristic (estimated distance from current to end node)
        # f: Total cost of node (f = g + h)

        # List of all nodes
        # unvisited_nodes = self.graph_flat.copy()

        nodes_to_visit = priorityqueue.PriorityQueue()
        nodes_to_visit.enqueue(start_node, 0)

        # Best-known cost to all nodes
        shortest_path = {}
        prev_nodes = {}

        shortest_path[start_node] = 0
        prev_nodes[start_node] = None

        while not nodes_to_visit.empty():
            current_node = nodes_to_visit.dequeue()
            current_node.visit()
            self.draw()
            if current_node == end_node:
                break

            for neighbour in current_node.neighbours:
                g = shortest_path[current_node] + 1
                if neighbour not in shortest_path or g < shortest_path[neighbour]:
                    shortest_path[neighbour] = g
                    f = g + AStarSearch.__calculate_heuristic(neighbour, end_node)
                    nodes_to_visit.enqueue(neighbour, f)
                    prev_nodes[neighbour] = current_node

        return prev_nodes, shortest_path

    def display_path_from_prev_nodes(self, prev_nodes: dict[PathfindingTile, PathfindingTile]) -> None:
        """
        COPIED FROM DIJKSTRA'S - THIS CAN BE DONE BETTER XD
        :param prev_nodes:
        :return:
        """
        x, y = self._start_pos
        start_node = self.map_tiles[x][y]
        x, y = self._end_pos
        end_node = self.map_tiles[x][y]

        current_node = end_node

        start_node.color = (7, 138, 0)

        while current_node != start_node:
            # GREEN
            current_node.color = (7, 138, 0)
            current_node = prev_nodes[current_node]
            self.draw()

    def solve(self) -> None:
        x, y = self._start_pos
        start_node = self.map_tiles[x][y]
        x, y = self._end_pos
        end_node = self.map_tiles[x][y]
        prev_nodes, _ = self.__a_star(start_node, end_node)
        self._frame_time = 0.05
        self.display_path_from_prev_nodes(prev_nodes)
        self.complete = True
