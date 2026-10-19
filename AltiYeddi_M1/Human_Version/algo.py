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
    
    # ==========================================
    # BREADTH-FIRST SEARCH (BFS) ALGORITHM
    # ==========================================
    def bfs(self, problem):

        #variables:
        #- name: Stores the string title of the search algorithm
        #- start: The initial State object retrieved from the problem instance
        #- frontier: A FIFO double ended queue that holds states waiting to be explored
        #- explored: A set keeping track of all states that have already been expanded to prevent infinite loops
        #- parent: A dictionary mapping each state to the predecessor state that discovered it (used for path reconstruction)
        #- cost_so_far: A dictionary tracking the accumulated path cost from the start node to each state
        #- order: A list recording the exact sequence of expanded nodes for GUI visualization
        #- current: The state currently being evaluated and expanded
        #- child: A neighboring valid state generated from the current state in problem.successors()
        
        name = "Breadth-First Search"
        start = problem.initial_state()

        #check if the starting state is already the goal
        if problem.goal_test(start):
            return self._success(name, start, {start: None}, [start], cost=0)

        frontier = deque([start])
        explored = set()
        parent = {start: None}
        cost_so_far = {start: 0}
        order = []

        while frontier:
            #popping off the oldest node from the left of the queue (FIFO)
            current = frontier.popleft()
            if current in explored:
                continue
            explored.add(current)
            order.append(current)

            #test if the current state satisfies the goal condition
            if problem.goal_test(current):
                return self._success(name, current, parent, order, cost=cost_so_far[current])

            #generate and evaluate all valid neighboring child states
            for child in problem.successors(current):
                if child not in explored and child not in parent:
                    parent[child] = current
                    cost_so_far[child] = cost_so_far[current] + problem.step_cost(current, child)
                    frontier.append(child)

        return self._failure(name, order)

        #create code to implement Breadth-First Search
        #return self._not_implemented("Breadth-First Search")
    #------------------------------------------------------------------------

    # ==========================================
    # DEPTH-FIRST SEARCH (DFS) ALGORITHM
    # ==========================================
    def dfs(self, problem):
        #variables:
        #- name: Stores the string title of the search algorithm
        #- start: The initial State object retrieved from the problem instance
        #- frontier: A LIFO list acting as a stack for states
        #- explored: A set keeping track of states that have already been expanded
        #- parent: A dictionary mapping each state to its parent state for path building
        #- cost_so_far: A dictionary tracking the cumulative cost to reach each state
        #- order: A list recording the sequence in which nodes are expanded
        #- current: The state popped from the top of the stack for expansion
        #- child: A neighboring state generated from the current state

        name = "Depth-First Search"
        start = problem.initial_state()
        
        # Check if start is goal
        if problem.goal_test(start):
            return self._success(name, start, {start: None}, [start], cost=0)

        frontier = [start]
        explored = set()
        parent = {start: None}
        cost_so_far = {start: 0}
        order = []

        while frontier:
            #popping the newest node from the end of the list (acting like a LIFO stack behavior)
            current = frontier.pop()
            
            if current in explored:
                continue
            
            explored.add(current)
            order.append(current)

            #check if goal is reached
            if problem.goal_test(current):
                return self._success(name, current, parent, order, cost=cost_so_far[current])

            #iterate through successors and push to stack
            for child in problem.successors(current):
                if child not in explored:
                    if child not in parent:
                        parent[child] = current
                        cost_so_far[child] = cost_so_far[current] + problem.step_cost(current, child)
                    frontier.append(child)

        return self._failure(name, order)

        #create code to implement Depth-First Search
        #return self._not_implemented("Depth-First Search")
    #------------------------------------------------------------------------
    
    # ==========================================
    # DIJKSTRA SEARCH
    # ==========================================
    def ucs(self, problem):
        #variables
        #- name: Stores the string title of the search algorithm
        #- start: The initial State object retrieved from the problem
        #- counter: An iterator from itertools.count() used as a tie-breaker in the priority queue to prevent comparison errors between states
        #- frontier: A priority queue (min-heap) storing tuples of `(cumulative_cost, tie_breaker, state)`
        #- explored: A set of states that have been expanded with their optimal path costs
        #- parent: A dictionary mapping each state to its optimal parent state
        #- g_cost: A dictionary storing the lowest known exact path cost from start to each state
        #- order: A list recording the node expansion sequence
        #- current: The state with the lowest cumulative cost extracted from the min-heap

        name = "Uniform-Cost Search"
        start = problem.initial_state()

        counter = count()
        # Priority queue stores tuples: (g_cost, tie_breaker, state)
        frontier = [(0, next(counter), start)]
        explored = set()
        parent = {start: None}
        g_cost = {start: 0}
        order = []

        while frontier:
            cost, _, current = heapq.heappop(frontier)

            if current in explored:
                continue
            explored.add(current)
            order.append(current)

            if problem.goal_test(current):
                return self._success(name, current, parent, order, cost=g_cost[current])

            for child in problem.successors(current):
                new_cost = g_cost[current] + problem.step_cost(current, child)
                if child not in explored and (child not in g_cost or new_cost < g_cost[child]):
                    g_cost[child] = new_cost
                    parent[child] = current
                    heapq.heappush(frontier, (new_cost, next(counter), child))

        return self._failure(name, order)
        #create code to implement Dijkstra's Search
        #return self._not_implemented("Dijkstra's Search")
    #------------------------------------------------------------------------
    
    # ==========================================
    # GREEDY BEST-FIRST SEARCH ALGORITHM
    # ==========================================
    def greedy(self, problem):
        #variables
        # - name: Stores the string title of the search algorithm
        # - start: The initial State object
        # - counter: An iterator used as a tie-breaker in the priority queue
        # - frontier: A priority queue (min-heap) storing tuples of (heuristic_value, tie_breaker, state)
        # - explored: A set of states that have already been expanded.
        # - parent: A dictionary mapping each state to its parent state
        # - g_cost: A dictionary tracking actual path costs.
        # - order: A list recording the node expansion sequence.
        # - current: The state with the lowest heuristic value h(n) extracted from the priority queue.

        name = "Greedy Best-First Search"
        start = problem.initial_state()

        counter = count()
        # Priority queue stores tuples: (heuristic_value, tie_breaker, state)
        frontier = [(problem.heuristic(start), next(counter), start)]
        explored = set()
        parent = {start: None}
        g_cost = {start: 0}
        order = []

        while frontier:
            _, _, current = heapq.heappop(frontier)

            if current in explored:
                continue
            explored.add(current)
            order.append(current)

            if problem.goal_test(current):
                return self._success(name, current, parent, order, cost=g_cost[current])

            for child in problem.successors(current):
                new_cost = g_cost[current] + problem.step_cost(current, child)
                if child not in explored:
                    if child not in parent:
                        parent[child] = current
                        g_cost[child] = new_cost
                    elif new_cost < g_cost[child]:
                        g_cost[child] = new_cost
                        parent[child] = current
                    heapq.heappush(frontier, (problem.heuristic(child), next(counter), child))

        return self._failure(name, order)

        #create code to implement Greedy Search
        #return self._not_implemented("Greedy Best-First Search")
    #------------------------------------------------------------------------
    
    # ==========================================
    # A* SEARCH ALGORITHM
    # ==========================================
    def astar(self, problem):
        # varaibles
        # - name: Stores the string title of the search algorithm
        # - start: The initial State object
        # - counter: An iterator used as a priority queue tie-breaker
        # - g_cost: A dictionary storing the exact cost from the start state to each state
        # - h_start: The heuristic estimate from the start state to the goal
        # - frontier: A priority queue (min-heap) storing tuples of (f_cost, tie_breaker, state) where f(n) = g(n) + h(n)
        # - explored: A set of fully expanded states
        # - parent: A dictionary tracking parent pointers for path reconstruction
        # - order: A list recording the node expansion sequence
        # - current: The state with the lowest total estimated evaluation cost f(n)

        name = "A* Search"
        start = problem.initial_state()

        counter = count()
        g_cost = {start: 0}
        h_start = problem.heuristic(start)
        # Priority queue stores tuples: (f_cost, tie_breaker, state) where f_cost = g_cost + heuristic
        frontier = [(g_cost[start] + h_start, next(counter), start)]
        explored = set()
        parent = {start: None}
        order = []

        while frontier:
            _, _, current = heapq.heappop(frontier)

            if current in explored:
                continue
            explored.add(current)
            order.append(current)

            if problem.goal_test(current):
                return self._success(name, current, parent, order, cost=g_cost[current])

            for child in problem.successors(current):
                new_cost = g_cost[current] + problem.step_cost(current, child)
                if child not in explored and (child not in g_cost or new_cost < g_cost[child]):
                    g_cost[child] = new_cost
                    parent[child] = current
                    f_cost = new_cost + problem.heuristic(child)
                    heapq.heappush(frontier, (f_cost, next(counter), child))

        return self._failure(name, order)
        
        #create code to implement A* Search
        #return self._not_implemented("A* Search")
    #------------------------------------------------------------------------

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
