from __future__ import annotations

from simplesearches import ShowPathfindingGUI, PathfindingTile

LARGE_VALUE = 1000000


class DijkstraAlgoSearch(ShowPathfindingGUI):
    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height, "Dijkstra's Algorithm", frame_time=0)
        self.draw()
        self.graph_flat = DijkstraAlgoSearch.flatten_tiles_map(self.map_tiles)

    def __dijkstra_algorithm(self, start_node: PathfindingTile) \
            -> tuple[dict[PathfindingTile, PathfindingTile], dict[PathfindingTile, int]]:
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
        prev_nodes, _ = self.__dijkstra_algorithm(start_node)
        self._frame_time = 0.05
        self.display_path_from_prev_nodes(prev_nodes)
        self.complete = True
