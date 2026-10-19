"""ALGORITHM FILE: reference algorithms plus the student work area."""

import heapq
import time
from collections import deque
from itertools import count
from search_result import SearchResult


class Algorithms:
    NAMES = (
        "Breadth-First Search",
        "Depth-First Search",
        "Uniform-Cost Search",
        "Greedy Best-First Search",
        "A* Search",
    )

    def solve(self, problem, name):
        methods = {
            self.NAMES[0]: self.bfs,
            self.NAMES[1]: self.dfs,
            self.NAMES[2]: self.ucs,
            self.NAMES[3]: self.greedy,
            self.NAMES[4]: self.astar,
        }
        if name not in methods:
            return SearchResult(name, success=False, message="Unknown algorithm.")

        # Time only the algorithm. The GUI animation is not included.
        start_time = time.perf_counter()
        result = methods[name](problem)
        elapsed_time = time.perf_counter() - start_time

        # This also protects the interface if a student temporarily uses pass.
        if result is None:
            result = SearchResult(
                name,
                success=False,
                message=f"{name} has not been implemented yet.",
            )

        result.runtime_seconds = elapsed_time
        return result

    def _not_implemented(self, name):
        return SearchResult(
            algorithm_name=name,
            success=False,
            message=f"{name} has not been implemented yet."
        )

    def bfs(self, problem):
        #create code to implement Breadth-First Search
        return self._not_implemented("Breadth-First Search")

    def dfs(self, problem):
        #create code to implement Depth-First Search
        return self._not_implemented("Depth-First Search")

    def ucs(self, problem):
        #create code to implement Dijkstra's Search
        return self._not_implemented("Dijkstra's Search")

    def greedy(self, problem):
        #create code to implement Greedy Search
        return self._not_implemented("Greedy Best-First Search")

    def astar(self, problem):
        #create code to implement A* Search
        return self._not_implemented("A* Search")

    def _success(self, name, goal, parent, order, cost=None):
        path, current = [], goal
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()
        return SearchResult(
            name, path, order, len(order),
            len(path) - 1 if cost is None else cost,
            True, "Solution found."
        )

    @staticmethod
    def _failure(name, order):
        return SearchResult(
            name, search_order=order, nodes_expanded=len(order),
            success=False, message="No solution found."
        )
