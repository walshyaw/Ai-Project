import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from algo import Algorithms
from escape_room import EscapeRoom

CELL, DELAY = 54, 250
COLORS = {"#":"#2B2238", ".":"#EEE9F5", "S":"#77C879", "E":"#7E57C2", "K":"#F4C542", "D":"#B23A48", "T":"#FFCA3A"}
LABELS = {"S":"START", "E":"EXIT", "K":"KEY", "D":"DOOR", "T":"TREASURE"}


class EscapeRoomGUI:
    def __init__(self, root):
        self.root = root
        root.title("CSC 3250 AI Escape Room")
        root.configure(bg="#F7F3FB")
        self.algorithms = Algorithms()
        self.problem = self.result = self.job = None
        self.running = False
        self.search_index = self.path_index = 0
        self.visited, self.path_tiles = set(), set()
        self.agent_position = None
        self.choice = tk.StringVar(value=Algorithms.NAMES[0])
        self.status = tk.StringVar(value="Load a map to begin.")
        self.algorithm = tk.StringVar(value="Algorithm: Not run")
        self.nodes = tk.StringVar(value="Nodes expanded: 0")
        self.cost = tk.StringVar(value="Path cost: 0")
        self.runtime = tk.StringVar(value="Runtime: 0.000000000 sec")
        self.key = tk.StringVar(value="Key collected: No")
        self.build()
        default = Path(__file__).resolve().parent / "maps" / "practice_map.json"
        if default.exists():
            self.load_map(default)

    def build(self):
        tk.Label(self.root, text="CSC 3250 AI ESCAPE ROOM", font=("Helvetica",22,"bold"), bg="#4B2E66", fg="white", pady=12).pack(fill="x")
        bar = tk.Frame(self.root, bg="#DDD1E8", padx=10, pady=10); bar.pack(fill="x")
        tk.Label(bar, text="Algorithm:", font=("Helvetica",11,"bold"), bg="#DDD1E8").pack(side="left", padx=(0,5))
        menu = ttk.Combobox(bar, textvariable=self.choice, values=Algorithms.NAMES, state="readonly", width=27)
        menu.pack(side="left", padx=(0,10)); menu.bind("<<ComboboxSelected>>", self.changed)
        for text, command in (("Step",self.step_clicked),("Start AI",self.start_ai),("Reset",self.reset),("Load Map",self.load_dialog)):
            tk.Button(bar,text=text,command=command,font=("Helvetica",11,"bold"),bg="#6F42A1",fg="white",relief="flat",padx=13,pady=7).pack(side="left",padx=4)
        body = tk.Frame(self.root,bg="#F7F3FB",padx=12,pady=12); body.pack(fill="both",expand=True)
        self.canvas = tk.Canvas(body,bg="#1F1828",highlightthickness=0); self.canvas.pack(side="left",fill="both",expand=True)
        side = tk.Frame(body,bg="white",width=290,padx=14,pady=14); side.pack(side="right",fill="y",padx=(12,0)); side.pack_propagate(False)
        tk.Label(side,text="MISSION",font=("Helvetica",14,"bold"),bg="white",fg="#4B2E66").pack(anchor="w")
        tk.Label(side,text="Select an algorithm, then use Step or Start AI. The door requires the key. Students edit algo.py only.",justify="left",wraplength=255,bg="white").pack(anchor="w",pady=(6,18))
        tk.Label(side,text="CURRENT RUN",font=("Helvetica",14,"bold"),bg="white",fg="#4B2E66").pack(anchor="w")
        for variable in (self.algorithm,self.nodes,self.cost,self.runtime,self.key):
            tk.Label(side,textvariable=variable,justify="left",wraplength=255,bg="white").pack(anchor="w",pady=2)
        tk.Label(side,text="STATUS",font=("Helvetica",14,"bold"),bg="white",fg="#4B2E66").pack(anchor="w",pady=(18,0))
        tk.Label(side,textvariable=self.status,justify="left",wraplength=255,bg="white").pack(anchor="w",pady=(6,0))

    def changed(self, event=None):
        self.reset(); self.status.set(f"Selected {self.choice.get()}. Click Step or Start AI.")

    def load_dialog(self):
        filename = filedialog.askopenfilename(title="Choose map",filetypes=[("JSON maps","*.json")])
        if filename: self.load_map(filename)

    def load_map(self, filename):
        try:
            self.problem = EscapeRoom(filename); self.reset(); self.status.set(f"Loaded {self.problem.name}.")
        except Exception as error:
            messagebox.showerror("Map Error", str(error))

    def reset(self):

        self.cancel()

        if not self.problem:
            return

        try:
            self.result = self.algorithms.solve(
                self.problem,
                self.choice.get()
            )

        except Exception as error:

            messagebox.showerror(
                "Algorithm Error",
                str(error)
            )

            return

        self.agent_position = (
            self.problem.start_position
        )

        self.search_index = 0
        self.path_index = 0

        self.visited = set()
        self.path_tiles = set()

        if self.result:
            self.algorithm.set(
                f"Algorithm: {self.result.algorithm_name}"
            )
            self.runtime.set(
                f"Runtime: {self.result.runtime_seconds:.9f} sec"
            )

            self.status.set(
                self.result.message
            )

        self.draw()

    def step_clicked(self): self.cancel(); self.step()

    def start_ai(self):
        if not self.result:
            self.status.set(
                "No algorithm result available."
            )
            return

        if not self.result.success:
            self.status.set(
                self.result.message
            )
            return

        if not self.running:
            self.running = True
            self.animate()

    def animate(self):
        if self.running and self.step(): self.job = self.root.after(DELAY,self.animate)
        else: self.running=False; self.job=None

    def step(self):
        if not self.result or not self.result.success: return False
        if self.search_index < len(self.result.search_order):
            state=self.result.search_order[self.search_index]; self.visited.add((state.row,state.column)); self.search_index+=1
            self.nodes.set(f"Nodes expanded: {self.search_index}"); self.status.set("Searching..."); self.draw(); return True
        if self.path_index < len(self.result.path):
            state=self.result.path[self.path_index]; self.agent_position=(state.row,state.column); self.path_tiles.add(self.agent_position); self.path_index+=1
            self.cost.set(f"Path cost: {max(0,self.path_index-1)}"); self.key.set(f"Key collected: {'Yes' if state.has_key else 'No'}")
            self.status.set("Escaped successfully!" if self.problem.goal_test(state) else "Following solution path..."); self.draw(); return True
        return False

    def cancel(self):
        self.running=False
        if self.job is not None:
            try: self.root.after_cancel(self.job)
            except tk.TclError: pass
            self.job=None

    def draw(self):
        self.canvas.delete("all")
        if not self.problem: return
        self.canvas.config(width=self.problem.column_count*CELL,height=self.problem.row_count*CELL)
        for row in range(self.problem.row_count):
            for column in range(self.problem.column_count):
                tile=self.problem.tile_at(row,column); location=(row,column); color=COLORS.get(tile,COLORS["."])
                if tile != "#" and location in self.visited: color="#C7B7DF"
                if tile != "#" and location in self.path_tiles: color="#80CBC4"
                x1,y1=column*CELL,row*CELL
                self.canvas.create_rectangle(x1,y1,x1+CELL,y1+CELL,fill=color,outline="#7B6A91")
                if tile in LABELS:
                    self.canvas.create_text(x1+CELL/2,y1+CELL/2,text=LABELS[tile],fill="white" if tile in "DE" else "#2B2238",font=("Helvetica",8,"bold"))
        if self.agent_position:
            row,column=self.agent_position; x1,y1=column*CELL+10,row*CELL+10
            self.canvas.create_oval(x1,y1,x1+CELL-20,y1+CELL-20,fill="#32224F",outline="white",width=2)
            self.canvas.create_text(x1+(CELL-20)/2,y1+(CELL-20)/2,text="AI",fill="white",font=("Helvetica",10,"bold"))
	

if __name__ == "__main__":
    root = tk.Tk()
    app = EscapeRoomGUI(root)
    root.mainloop()
