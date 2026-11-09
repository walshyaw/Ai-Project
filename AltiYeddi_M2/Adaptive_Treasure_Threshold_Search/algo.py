"""ALGORITHM FILE: reference algorithms plus the student work area.

Milestone 2 layout:
- The five Milestone 1 algorithms (BFS, DFS, UCS, Greedy, A*) are preserved
  unchanged from AltiYeddi_M1/Human_Version so they can be re-run as
  comparison baselines on the same Milestone 2 maps (Part 3 requirement).
- Adaptive Treasure Threshold Search (Part 2, the team-designed algorithm)
  is added below.
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
        "Adaptive Treasure Threshold Search",
    )

    def solve(self, problem, name):
        methods = {
            self.NAMES[0]: self.bfs,
            self.NAMES[1]: self.dfs,
            self.NAMES[2]: self.ucs,
            self.NAMES[3]: self.greedy,
            self.NAMES[4]: self.astar,
            self.NAMES[5]: self.atts,
        }
        if name not in methods:
            return SearchResult(name, success=False, message="Unknown algorithm.")

        start_time = time.perf_counter()
        result = methods[name](problem)
        elapsed_time = time.perf_counter() - start_time

        if result is None:
            result = SearchResult(
                name, success=False, message=f"{name} has not been implemented yet."
            )
        result.runtime_seconds = elapsed_time
        return result

    def _not_implemented(self, name):
        return SearchResult(
            algorithm_name=name,
            success=False,
            message=f"{name} has not been implemented yet.",
        )

    # ------------------------------------------------------------------
    # Milestone 1 baselines (Part 3 comparison), reused from the team's
    # Human_Version algo.py without changes.
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Milestone 2, Part 2: team-designed algorithm (implemented by Shlok).
    # ------------------------------------------------------------------

    def atts(self, problem):
        """Adaptive Treasure Threshold Search.

        The algorithm intentionally requires the key before accepting the exit.
        The project's State object already remembers key possession, while ATTS
        separately tracks treasure locations so it remains compatible with the
        professor's existing State and GUI classes.
        """
        name = "Adaptive Treasure Threshold Search"
        start = problem.initial_state()
        tie_breaker = count()

        treasure_reward = 3.0
        key_reward = 8.0
        nearby_treasure_reward = 1.5
        treasure_ratio_threshold = 0.25

        treasures = {
            (row, column)
            for row in range(problem.row_count)
            for column in range(problem.column_count)
            if problem.tile_at(row, column) == "T"
        }

        start_treasures = frozenset()
        start_id = (start.row, start.column, start.has_key, start_treasures)

        frontier = []
        heapq.heappush(
            frontier, (0.0, next(tie_breaker), start, start_treasures, 0)
        )

        best_cost = {start_id: 0}
        parent = {start_id: None}
        state_for = {start_id: start}
        search_order = []

        while frontier:
            _, _, current, collected, current_cost = heapq.heappop(frontier)
            current_id = (
                current.row,
                current.column,
                current.has_key,
                collected,
            )

            if current_cost != best_cost.get(current_id):
                continue

            search_order.append(current)

            # Part 2 requirement for this custom strategy: do not accept the
            # exit until the key has actually been collected.
            if problem.goal_test(current) and current.has_key:
                path = []
                trace = current_id
                while trace is not None:
                    path.append(state_for[trace])
                    trace = parent[trace]
                path.reverse()

                return SearchResult(
                    algorithm_name=name,
                    path=path,
                    search_order=search_order,
                    nodes_expanded=len(search_order),
                    path_cost=current_cost,
                    success=True,
                    message=(
                        "Solution found with key. "
                        f"Treasures collected: {len(collected)}."
                    ),
                )

            for child in problem.successors(current):
                location = (child.row, child.column)
                child_collected = collected
                if location in treasures:
                    child_collected = collected | {location}

                new_cost = current_cost + problem.step_cost(current, child)
                child_id = (
                    child.row,
                    child.column,
                    child.has_key,
                    child_collected,
                )

                if new_cost >= best_cost.get(child_id, float("inf")):
                    continue

                # Before the key is collected, reduce exit pressure. Once the
                # key is held, strongly prioritize getting to the exit.
                exit_weight = 0.6 if not child.has_key else 2.0
                if child.has_key and child_collected:
                    exit_weight = 2.2

                key_bonus = key_reward if child.has_key else 0.0
                collected_value = len(child_collected)

                best_treasure_ratio = 0.0
                remaining = treasures - set(child_collected)
                for tr, tc in remaining:
                    distance = abs(child.row - tr) + abs(child.column - tc)
                    ratio = 1.0 / (distance + 1)
                    if ratio >= treasure_ratio_threshold:
                        best_treasure_ratio = max(best_treasure_ratio, ratio)

                priority = (
                    new_cost
                    + exit_weight * problem.heuristic(child)
                    - key_bonus
                    - treasure_reward * collected_value
                    - nearby_treasure_reward * best_treasure_ratio
                )

                best_cost[child_id] = new_cost
                parent[child_id] = current_id
                state_for[child_id] = child
                heapq.heappush(
                    frontier,
                    (
                        priority,
                        next(tie_breaker),
                        child,
                        child_collected,
                        new_cost,
                    ),
                )

        return self._failure(name, search_order)

    def _success(self, name, goal, parent, order, cost=None):
        path, current = [], goal
        while current is not None:
            path.append(current)
            current = parent[current]
        path.reverse()
        return SearchResult(
            name,
            path,
            order,
            len(order),
            len(path) - 1 if cost is None else cost,
            True,
            "Solution found.",
        )

    @staticmethod
    def _failure(name, order):
        return SearchResult(
            name,
            search_order=order,
            nodes_expanded=len(order),
            success=False,
            message="No solution found.",
        )
