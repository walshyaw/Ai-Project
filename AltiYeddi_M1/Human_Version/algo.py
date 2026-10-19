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

        # Time only the selected search algorithm. GUI animation is excluded.
        start_time = time.perf_counter()
        result = methods[name](problem)
        elapsed_time = time.perf_counter() - start_time

        # A method containing only pass returns None. Keep the map usable while
        # students are still implementing that algorithm.
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
        name = "Breadth-First Search"
        start = problem.initial_state()
        frontier = deque([start])
        visited = {start}
        parent = {start: None}
        costs = {start: 0}
        order = []

        while frontier:
            # The queue makes us explore the oldest waiting state first.
            current = frontier.popleft()
            order.append(current)

            if problem.goal_test(current):
                return self._success(name, current, parent, order, costs[current])

            for child in problem.successors(current):
                if child not in visited:
                    visited.add(child)
                    parent[child] = current
                    costs[child] = costs[current] + problem.step_cost(current, child)
                    frontier.append(child)

        return self._failure(name, order)

    def dfs(self, problem):
        name = "Depth-First Search"
        start = problem.initial_state()
        frontier = [start]
        visited = {start}
        parent = {start: None}
        costs = {start: 0}
        order = []

        while frontier:
            # The stack makes us explore the newest waiting state first.
            current = frontier.pop()
            order.append(current)

            if problem.goal_test(current):
                return self._success(name, current, parent, order, costs[current])

            for child in problem.successors(current):
                if child not in visited:
                    visited.add(child)
                    parent[child] = current
                    costs[child] = costs[current] + problem.step_cost(current, child)
                    frontier.append(child)

        return self._failure(name, order)

    def ucs(self, problem):
        name = "Uniform-Cost Search"
        start = problem.initial_state()
        frontier = [(0, start)]
        costs = {start: 0}
        parent = {start: None}
        visited = set()
        order = []

        while frontier:
            # Find the state with the lowest path cost in the frontier.
            lowest_index = 0
            for i in range(1, len(frontier)):
                if frontier[i][0] < frontier[lowest_index][0]:
                    lowest_index = i

            cost, current = frontier.pop(lowest_index)

            if current in visited:
                continue
            visited.add(current)
            order.append(current)

            if problem.goal_test(current):
                return self._success(name, current, parent, order, cost)

            for child in problem.successors(current):
                new_cost = cost + problem.step_cost(current, child)
                # Only add this route if it is cheaper than the best one found so far.
                if child not in visited and new_cost < costs.get(child, float("inf")):
                    costs[child] = new_cost
                    parent[child] = current
                    frontier.append((new_cost, child))

        return self._failure(name, order)

    def greedy(self, problem):
        name = "Greedy Best-First Search"
        start = problem.initial_state()
        frontier = [(problem.heuristic(start), start)]
        parent = {start: None}
        costs = {start: 0}
        visited = set()
        order = []

        while frontier:
            # Greedy search picks the state that seems closest to the goal.
            lowest_index = 0
            for i in range(1, len(frontier)):
                if frontier[i][0] < frontier[lowest_index][0]:
                    lowest_index = i

            _, current = frontier.pop(lowest_index)

            if current in visited:
                continue
            visited.add(current)
            order.append(current)

            if problem.goal_test(current):
                return self._success(name, current, parent, order, costs[current])

            for child in problem.successors(current):
                if child not in visited and child not in parent:
                    parent[child] = current
                    costs[child] = costs[current] + problem.step_cost(current, child)
                    frontier.append((problem.heuristic(child), child))

        return self._failure(name, order)

    def astar(self, problem):
        name = "A* Search"
        start = problem.initial_state()
        frontier = [(problem.heuristic(start), start)]
        costs = {start: 0}
        parent = {start: None}
        visited = set()
        order = []

        while frontier:
            # Find the state with the smallest estimated total cost.
            lowest_index = 0
            for i in range(1, len(frontier)):
                if frontier[i][0] < frontier[lowest_index][0]:
                    lowest_index = i

            _, current = frontier.pop(lowest_index)

            if current in visited:
                continue
            visited.add(current)
            order.append(current)

            if problem.goal_test(current):
                return self._success(name, current, parent, order, costs[current])

            for child in problem.successors(current):
                new_cost = costs[current] + problem.step_cost(current, child)
                if child not in visited and new_cost < costs.get(child, float("inf")):
                    costs[child] = new_cost
                    parent[child] = current
                    total_cost = new_cost + problem.heuristic(child)
                    frontier.append((total_cost, child))

        return self._failure(name, order)

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
