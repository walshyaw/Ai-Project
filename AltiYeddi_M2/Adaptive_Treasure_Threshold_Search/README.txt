CSC 3250 AI ESCAPE ROOM

RUNNING THE PROJECT
Windows:
    python run.py

macOS/Linux:
    python3 run.py

The project folder must contain:
    run.py
    algo.py
    escape_gui.py
    escape_room.py
    search_result.py
    state.py
    maps/practice_map.json

ALGORITHMS
The dropdown includes BFS, DFS, UCS, Greedy Best-First, A*, and Adaptive Treasure Threshold Search.
Student search algorithms are implemented in algo.py.

TIMING
Algorithms.solve measures only the selected search method using time.perf_counter().
The GUI animation delay is not included in runtime.
Runtime is displayed in the CURRENT RUN panel as soon as the algorithm finishes computing.
Because the included maps are small, valid runtimes may be less than one millisecond. The GUI displays nine decimal places so these small values remain visible.

CURRENT RUN VALUES
Nodes expanded is animated during the search and ends at SearchResult.nodes_expanded.
Path cost is animated along the solution and ends at SearchResult.path_cost.
Runtime comes from SearchResult.runtime_seconds and does not increase during animation.
