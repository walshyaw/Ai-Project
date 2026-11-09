"""ALGORITHM FILE: reference algorithms plus the student work area.

Milestone 2 layout:
- The five Milestone 1 algorithms (BFS, DFS, UCS, Greedy, A*) are preserved
  unchanged from AltiYeddi_M1/Human_Version so they can be re-run as
  comparison baselines on the same Milestone 2 maps (Part 3 requirement).
- Weighted A* Search (Part 1, the chosen known algorithm) is added below.
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
        "Weighted A* Search",
    )

    def solve(self, problem, name):
        methods = {
            self.NAMES[0]: self.bfs,
            self.NAMES[1]: self.dfs,
            self.NAMES[2]: self.ucs,
            self.NAMES[3]: self.greedy,
            self.NAMES[4]: self.astar,
            self.NAMES[5]: self.weighted_astar,
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
    # Milestone 2, Part 1: chosen known algorithm (implemented by Alex).
    # ------------------------------------------------------------------

    def weighted_astar(self, problem):

        """
        Weighted A* Search.

        The algorithm trades optimality for speed by multiplying the heuristic 
        by a weight factor (w > 1). By prioritizing nodes that appear closer to 
        the goal, it expands fewer nodes and reaches the exit faster than standard 
        A*. It integrates directly with the professor's existing problem.heuristic() 
        method and uses a standard priority queue to ensure compatibility with 
        the existing GUI and search
        """

        weight = 2.0  #chosen weight to prioritize heuristic speed over optimal path

        start_state = problem.initial_state()
        if problem.goal_test(start_state):
            return self._success("Weighted A* Search", start_state, {start_state: None}, [start_state], 0)

        #priority queue: (f_cost, tie_breaker, g_cost, state, parent_state)
        #tie breaker ensures consistent behavior if f-costs are equal
        tie_breaker = count()
        frontier = []

        #initial push with the weighted heuristic
        initial_h = problem.heuristic(start_state)
        heapq.heappush(frontier, (weight * initial_h, next(tie_breaker), 0, start_state, None))

        explored = set()
        parent_map = {start_state: None}
        g_costs = {start_state: 0}
        search_order = []

        while frontier:
            f, _, g, current_state, parent = heapq.heappop(frontier)

            #skip if already expanded this state (handles cycles)
            if current_state in explored:
                continue

            explored.add(current_state)
            search_order.append(current_state)
            parent_map[current_state] = parent

            #goal test
            if problem.goal_test(current_state):
                return self._success("Weighted A* Search", current_state, parent_map, search_order, g)

            #expand successors
            for next_state in problem.successors(current_state):

                # Use the framework's step cost method
                step_cost = problem.step_cost(current_state, next_state)
                new_g = g + step_cost

                #if unvisited or we found a cheaper path to a previously seen state
                if next_state not in explored and (next_state not in g_costs or new_g < g_costs[next_state]):
                    g_costs[next_state] = new_g
                    h = problem.heuristic(next_state)
                    #core logic: weight * heuristic
                    new_f = new_g + (weight * h)
                    heapq.heappush(frontier, (new_f, next(tie_breaker), new_g, next_state, current_state))

        return self._failure("Weighted A* Search", search_order)

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
