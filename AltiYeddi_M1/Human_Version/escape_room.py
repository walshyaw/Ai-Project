import json
from pathlib import Path
from state import State


class EscapeRoom:
    DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))

    def __init__(self, filename):
        self.filename = Path(filename)
        with open(filename, encoding="utf-8") as file:
            data = json.load(file)
        rows = data["grid"]
        if not rows or len({len(row) for row in rows}) != 1:
            raise ValueError("The map must be nonempty and rectangular.")
        self.name = data.get("name", self.filename.stem)
        self.grid = [list(row) for row in rows]
        starts = [(r, c) for r, row in enumerate(self.grid) for c, tile in enumerate(row) if tile == "S"]
        exits = [(r, c) for r, row in enumerate(self.grid) for c, tile in enumerate(row) if tile == "E"]
        if len(starts) != 1 or len(exits) != 1:
            raise ValueError("The map must contain exactly one S and one E.")
        self.start_position, self.exit_position = starts[0], exits[0]

    @property
    def row_count(self):
        return len(self.grid)

    @property
    def column_count(self):
        return len(self.grid[0])

    def tile_at(self, row, column):
        return self.grid[row][column]

    def initial_state(self):
        return State(*self.start_position, False)

    def goal_test(self, state):
        return (state.row, state.column) == self.exit_position

    def successors(self, state):
        for dr, dc in self.DIRECTIONS:
            row, column = state.row + dr, state.column + dc
            if not (0 <= row < self.row_count and 0 <= column < self.column_count):
                continue
            tile = self.tile_at(row, column)
            if tile == "#":
                continue
            has_key = state.has_key or tile == "K"
            if tile == "D" and not has_key:
                continue
            yield State(row, column, has_key)

    def step_cost(self, current, child):
        return 1

    def heuristic(self, state):
        exit_row, exit_column = self.exit_position
        return abs(state.row - exit_row) + abs(state.column - exit_column)
