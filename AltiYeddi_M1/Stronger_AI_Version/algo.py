"""Search algorithms for the Escape Room framework.

The algorithms use only the supplied problem interface: initial_state(),
successors(state), goal_test(state), step_cost(current, child), and heuristic(state).
"""

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
        start_time = time.perf_counter()
        result = methods[name](problem)
        result.runtime_seconds = time.perf_counter() - start_time
        return result

    def bfs(self, problem):
        """Explore shallowest states first using a FIFO queue."""
        start = problem.initial_state()
        frontier = deque([start])
        discovered = {start}
        parent = {start: None}
        costs = {start: 0}
        order = []

        while frontier:
            current = frontier.popleft()
            order.append(current)
            if problem.goal_test(current):
                return self._success("Breadth-First Search", current, parent, order, costs[current])
            for child in problem.successors(current):
                if child in discovered:
                    continue
                discovered.add(child)
                parent[child] = current
                costs[child] = costs[current] + problem.step_cost(current, child)
                frontier.append(child)
        return self._failure("Breadth-First Search", order)

    def dfs(self, problem):
        """Explore one branch deeply before backtracking, using a LIFO stack."""
        start = problem.initial_state()
        frontier = [start]
        discovered = {start}
        parent = {start: None}
        costs = {start: 0}
        order = []

        while frontier:
            current = frontier.pop()
            order.append(current)
            if problem.goal_test(current):
                return self._success("Depth-First Search", current, parent, order, costs[current])
            # Reverse successors so the first yielded successor is explored first.
            children = list(problem.successors(current))
            for child in reversed(children):
                if child in discovered:
                    continue
                discovered.add(child)
                parent[child] = current
                costs[child] = costs[current] + problem.step_cost(current, child)
                frontier.append(child)
        return self._failure("Depth-First Search", order)

    def ucs(self, problem):
        """Always expand the frontier state with the lowest accumulated path cost."""
        start = problem.initial_state()
        tie = count()
        frontier = [(0, next(tie), start)]
        best_cost = {start: 0}
        parent = {start: None}
        order = []
        expanded_cost = {}

        while frontier:
            cost, _, current = heapq.heappop(frontier)
            if cost != best_cost.get(current):
                continue  # Ignore an outdated priority-queue entry.
            if current in expanded_cost and expanded_cost[current] <= cost:
                continue
            expanded_cost[current] = cost
            order.append(current)
            if problem.goal_test(current):
                return self._success("Uniform-Cost Search", current, parent, order, cost)
            for child in problem.successors(current):
                new_cost = cost + problem.step_cost(current, child)
                if new_cost < best_cost.get(child, float("inf")):
                    best_cost[child] = new_cost
                    parent[child] = current
                    heapq.heappush(frontier, (new_cost, next(tie), child))
        return self._failure("Uniform-Cost Search", order)

    def greedy(self, problem):
        """Choose the frontier state with the smallest heuristic estimate to the goal."""
        start = problem.initial_state()
        tie = count()
        frontier = [(problem.heuristic(start), next(tie), start)]
        discovered = {start}
        parent = {start: None}
        costs = {start: 0}
        order = []

        while frontier:
            _, _, current = heapq.heappop(frontier)
            order.append(current)
            if problem.goal_test(current):
                return self._success("Greedy Best-First Search", current, parent, order, costs[current])
            for child in problem.successors(current):
                if child in discovered:
                    continue
                discovered.add(child)
                parent[child] = current
                costs[child] = costs[current] + problem.step_cost(current, child)
                heapq.heappush(frontier, (problem.heuristic(child), next(tie), child))
        return self._failure("Greedy Best-First Search", order)

    def astar(self, problem):
        """Prioritize f(n) = g(n) + h(n), reopening a state if a cheaper route is found."""
        start = problem.initial_state()
        tie = count()
        start_cost = 0
        frontier = [(start_cost + problem.heuristic(start), next(tie), start_cost, start)]
        best_cost = {start: start_cost}
        parent = {start: None}
        order = []
        expanded_cost = {}

        while frontier:
            _, _, cost, current = heapq.heappop(frontier)
            if cost != best_cost.get(current):
                continue
            if current in expanded_cost and expanded_cost[current] <= cost:
                continue
            expanded_cost[current] = cost
            order.append(current)
            if problem.goal_test(current):
                return self._success("A* Search", current, parent, order, cost)
            for child in problem.successors(current):
                new_cost = cost + problem.step_cost(current, child)
                if new_cost < best_cost.get(child, float("inf")):
                    best_cost[child] = new_cost
                    parent[child] = current
                    priority = new_cost + problem.heuristic(child)
                    heapq.heappush(frontier, (priority, next(tie), new_cost, child))
        return self._failure("A* Search", order)

    @staticmethod
    def _success(name, goal, parent, order, cost=None):
        path = []
        current = goal
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()
        return SearchResult(
            algorithm_name=name,
            path=path,
            search_order=order,
            nodes_expanded=len(order),
            path_cost=cost if cost is not None else len(path) - 1,
            success=True,
            message="Solution found.",
        )

    @staticmethod
    def _failure(name, order):
        return SearchResult(
            algorithm_name=name,
            search_order=order,
            nodes_expanded=len(order),
            success=False,
            message="No solution found.",
        )
