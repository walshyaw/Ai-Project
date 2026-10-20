import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from algo import Algorithms
from escape_room import EscapeRoom


CELL = 54
MIN_CELL = 28
DELAY = 250

COLORS = {
    "#": "#2B2238",
    ".": "#EEE9F5",
    "S": "#77C879",
    "E": "#7E57C2",
    "K": "#F4C542",
    "D": "#B23A48",
    "T": "#FFCA3A",
}

LABELS = {
    "S": "START",
    "E": "EXIT",
    "K": "KEY",
    "D": "DOOR",
    "T": "TREASURE",
}


class EscapeRoomGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CSC 3250 AI Escape Room")
        self.root.configure(bg="#F7F3FB")

        self.algorithms = Algorithms()

        self.problem = None
        self.result = None
        self.job = None
        self.running = False

        self.search_index = 0
        self.path_index = 0

        self.visited = set()
        self.path_tiles = set()
        self.agent_position = None

        self.choice = tk.StringVar(
            value=Algorithms.NAMES[0]
        )

        self.status = tk.StringVar(
            value="Load a map to begin."
        )

        self.algorithm = tk.StringVar(
            value="Algorithm: Not run"
        )

        self.nodes = tk.StringVar(
            value="Nodes expanded: 0"
        )

        self.cost = tk.StringVar(
            value="Path cost: 0"
        )

        # The actual runtime remains hidden until the visual run finishes.
        self.runtime = tk.StringVar(
            value="Runtime: --"
        )

        self.key = tk.StringVar(
            value="Key collected: No"
        )

        self.build()

        default = (
            Path(__file__).resolve().parent
            / "maps"
            / "practice_map.json"
        )

        if default.exists():
            self.load_map(default)

    def build(self):
        tk.Label(
            self.root,
            text="CSC 3250 AI ESCAPE ROOM",
            font=("Helvetica", 22, "bold"),
            bg="#4B2E66",
            fg="white",
            pady=12,
        ).pack(fill="x")

        toolbar = tk.Frame(
            self.root,
            bg="#DDD1E8",
            padx=10,
            pady=10,
        )
        toolbar.pack(fill="x")

        tk.Label(
            toolbar,
            text="Algorithm:",
            font=("Helvetica", 11, "bold"),
            bg="#DDD1E8",
        ).pack(side="left", padx=(0, 5))

        menu = ttk.Combobox(
            toolbar,
            textvariable=self.choice,
            values=Algorithms.NAMES,
            state="readonly",
            width=27,
        )
        menu.pack(side="left", padx=(0, 10))
        menu.bind(
            "<<ComboboxSelected>>",
            self.changed,
        )

        buttons = (
            ("Step", self.step_clicked),
            ("Start AI", self.start_ai),
            ("Reset", self.reset),
            ("Load Map", self.load_dialog),
        )

        for text, command in buttons:
            tk.Button(
                toolbar,
                text=text,
                command=command,
                font=("Helvetica", 11, "bold"),
                bg="#6F42A1",
                fg="white",
                relief="flat",
                padx=13,
                pady=7,
            ).pack(side="left", padx=4)

        body = tk.Frame(
            self.root,
            bg="#F7F3FB",
            padx=12,
            pady=12,
        )
        body.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            body,
            bg="#1F1828",
            highlightthickness=0,
        )
        self.canvas.pack(
            side="left",
            fill="both",
            expand=True,
        )

        sidebar = tk.Frame(
            body,
            bg="white",
            width=290,
            padx=14,
            pady=14,
        )
        sidebar.pack(
            side="right",
            fill="y",
            padx=(12, 0),
        )
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="MISSION",
            font=("Helvetica", 14, "bold"),
            bg="white",
            fg="#4B2E66",
        ).pack(anchor="w")

        instructions = (
            "Select an algorithm, then use Step or Start AI. "
            "The door requires the key. Students edit algo.py only."
        )

        tk.Label(
            sidebar,
            text=instructions,
            justify="left",
            wraplength=255,
            bg="white",
        ).pack(anchor="w", pady=(6, 18))

        tk.Label(
            sidebar,
            text="CURRENT RUN",
            font=("Helvetica", 14, "bold"),
            bg="white",
            fg="#4B2E66",
        ).pack(anchor="w")

        for variable in (
            self.algorithm,
            self.nodes,
            self.cost,
            self.runtime,
            self.key,
        ):
            tk.Label(
                sidebar,
                textvariable=variable,
                justify="left",
                wraplength=255,
                bg="white",
            ).pack(anchor="w", pady=2)

        tk.Label(
            sidebar,
            text="STATUS",
            font=("Helvetica", 14, "bold"),
            bg="white",
            fg="#4B2E66",
        ).pack(anchor="w", pady=(18, 0))

        tk.Label(
            sidebar,
            textvariable=self.status,
            justify="left",
            wraplength=255,
            bg="white",
        ).pack(anchor="w", pady=(6, 0))

    def changed(self, event=None):
        self.reset()

        self.status.set(
            f"Selected {self.choice.get()}. "
            "Click Step or Start AI."
        )

    def load_dialog(self):
        filename = filedialog.askopenfilename(
            title="Choose map",
            filetypes=[
                ("JSON maps", "*.json")
            ],
        )

        if filename:
            self.load_map(filename)

    def load_map(self, filename):
        try:
            self.problem = EscapeRoom(filename)
            self.fit_map_to_screen()
            self.reset()

            self.status.set(
                f"Loaded {self.problem.name}."
            )

        except Exception as error:
            messagebox.showerror(
                "Map Error",
                str(error),
            )

    def reset(self):
        self.cancel()

        if not self.problem:
            return

        try:
            # The algorithm executes here so the GUI has the search order and
            # solution path to animate. Its time is hidden until the visual run
            # reaches the exit.
            self.result = self.algorithms.solve(
                self.problem,
                self.choice.get(),
            )

        except Exception as error:
            messagebox.showerror(
                "Algorithm Error",
                str(error),
            )
            return

        self.agent_position = self.problem.start_position

        self.search_index = 0
        self.path_index = 0

        self.visited = set()
        self.path_tiles = set()

        if self.result:
            self.algorithm.set(
                f"Algorithm: {self.result.algorithm_name}"
            )
        else:
            self.algorithm.set(
                f"Algorithm: {self.choice.get()}"
            )

        self.nodes.set(
            "Nodes expanded: 0"
        )

        self.cost.set(
            "Path cost: 0"
        )

        # Do not reveal the measured runtime during reset.
        self.runtime.set(
            "Runtime: --"
        )

        self.key.set(
            "Key collected: No"
        )

        if self.result and self.result.success:
            self.status.set(
                "Ready. Click Step or Start AI."
            )

        elif self.result:
            self.status.set(
                self.result.message
            )

        else:
            self.status.set(
                "No algorithm result is available."
            )

        self.draw()

    def step_clicked(self):
        self.cancel()
        self.step()

    def start_ai(self):
        if not self.result or not self.result.success:
            self.status.set(
                self.result.message
                if self.result
                else "No result."
            )
            return

        if not self.running:
            self.running = True
            self.animate()

    def animate(self):
        if not self.running:
            return

        more_steps = self.step()

        if more_steps:
            self.job = self.root.after(
                DELAY,
                self.animate,
            )

        else:
            self.running = False
            self.job = None
            self.show_final_results()

    def step(self):
        if not self.result or not self.result.success:
            return False

        # First animate the order in which states were expanded.
        if self.search_index < len(
            self.result.search_order
        ):
            state = self.result.search_order[
                self.search_index
            ]

            self.visited.add(
                (state.row, state.column)
            )

            self.search_index += 1

            self.nodes.set(
                f"Nodes expanded: {self.search_index}"
            )

            self.status.set(
                "Searching..."
            )

            self.draw()

            return True

        # Then animate the agent following the solution path.
        if self.path_index < len(
            self.result.path
        ):
            state = self.result.path[
                self.path_index
            ]

            self.agent_position = (
                state.row,
                state.column,
            )

            self.path_tiles.add(
                self.agent_position
            )

            self.path_index += 1

            self.cost.set(
                f"Path cost: {max(0, self.path_index - 1)}"
            )

            self.key.set(
                "Key collected: "
                f"{'Yes' if state.has_key else 'No'}"
            )

            if self.problem.goal_test(state):
                self.status.set(
                    "Escaped successfully!"
                )

                # Reveal runtime only after the agent reaches the exit.
                self.show_final_results()

            else:
                self.status.set(
                    "Following solution path..."
                )

            self.draw()

            return True

        self.show_final_results()

        return False

    def show_final_results(self):
        if not self.result:
            return

        self.nodes.set(
            f"Nodes expanded: {self.result.nodes_expanded}"
        )

        self.cost.set(
            f"Path cost: {self.result.path_cost}"
        )

        self.runtime.set(
            f"Runtime: {self.result.runtime_seconds:.9f} sec"
        )

    def cancel(self):
        self.running = False

        if self.job is not None:
            try:
                self.root.after_cancel(
                    self.job
                )
            except tk.TclError:
                pass

            self.job = None

    def draw(self):
        self.canvas.delete("all")

        if not self.problem:
            return

        self.canvas.config(
            width=self.problem.column_count * CELL,
            height=self.problem.row_count * CELL,
        )

        for row in range(
            self.problem.row_count
        ):
            for column in range(
                self.problem.column_count
            ):
                tile = self.problem.tile_at(
                    row,
                    column,
                )

                location = (
                    row,
                    column,
                )

                color = COLORS.get(
                    tile,
                    COLORS["."],
                )

                if (
                    tile != "#"
                    and location in self.visited
                ):
                    color = "#C7B7DF"

                if (
                    tile != "#"
                    and location in self.path_tiles
                ):
                    color = "#80CBC4"

                x1 = column * CELL
                y1 = row * CELL

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x1 + CELL,
                    y1 + CELL,
                    fill=color,
                    outline="#7B6A91",
                )

                if tile in LABELS:
                    self.canvas.create_text(
                        x1 + CELL / 2,
                        y1 + CELL / 2,
                        text=LABELS[tile],
                        fill=(
                            "white"
                            if tile in "DE"
                            else "#2B2238"
                        ),
                        font=(
                            "Helvetica",
                            8,
                            "bold",
                        ),
                    )

        if self.agent_position:
            row, column = self.agent_position

            padding = max(
                5,
                CELL // 5,
            )

            x1 = column * CELL + padding
            y1 = row * CELL + padding
            diameter = CELL - (2 * padding)

            self.canvas.create_oval(
                x1,
                y1,
                x1 + diameter,
                y1 + diameter,
                fill="#32224F",
                outline="white",
                width=2,
            )

            self.canvas.create_text(
                x1 + diameter / 2,
                y1 + diameter / 2,
                text="AI",
                fill="white",
                font=(
                    "Helvetica",
                    max(7, CELL // 5),
                    "bold",
                ),
            )

    def fit_map_to_screen(self):
        global CELL

        if not self.problem:
            return

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Reserve room for the sidebar, toolbar, title, and window borders.
        available_width = screen_width - 380
        available_height = screen_height - 230

        width_cell_size = (
            available_width
            // self.problem.column_count
        )

        height_cell_size = (
            available_height
            // self.problem.row_count
        )

        CELL = max(
            MIN_CELL,
            min(
                54,
                width_cell_size,
                height_cell_size,
            ),
        )
