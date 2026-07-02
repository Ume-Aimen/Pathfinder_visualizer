"""
main.py
-------
Tkinter GUI: draws the grid, handles mouse clicks (walls / start / goal),
lets the user pick an algorithm + heuristic, runs the search, and animates
frontier / visited / path colors while showing live metrics.

Run with:  python main.py
"""

import tkinter as tk
from tkinter import ttk, messagebox

from algorithms import ALGORITHMS
from heuristics import HEURISTICS
from maze_generator import generate_random_grid

CELL_SIZE = 28

COLORS = {
    "empty": "#ffffff",
    "wall": "#2b2b2b",
    "start": "#ff9800",
    "goal": "#e53935",
    "frontier": "#ffee58",   # yellow
    "visited": "#64b5f6",    # blue
    "path": "#43a047",       # green
    "grid_line": "#cccccc",
}

ANIMATION_DELAY_MS = 12  # speed of the visual playback 


class PathfinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pathfinding Visualizer - BFS / UCS / GBFS / A*")

        self.rows = 15
        self.cols = 20
        self.grid = [[0] * self.cols for _ in range(self.rows)]
        self.start = (2, 2)
        self.goal = (self.rows - 3, self.cols - 3)
        self.click_mode = tk.StringVar(value="wall")  # wall | start | goal

        self._build_controls()
        self._build_canvas()
        self.draw_grid()

    def _build_controls(self):
        panel = ttk.Frame(self.root, padding=8)
        panel.grid(row=0, column=0, sticky="ns")

        ttk.Label(panel, text="Grid size", font=("", 10, "bold")).pack(anchor="w")
        size_row = ttk.Frame(panel)
        size_row.pack(anchor="w", pady=(0, 8))
        self.rows_var = tk.IntVar(value=self.rows)
        self.cols_var = tk.IntVar(value=self.cols)
        ttk.Label(size_row, text="Rows").grid(row=0, column=0)
        ttk.Entry(size_row, textvariable=self.rows_var, width=5).grid(row=0, column=1, padx=4)
        ttk.Label(size_row, text="Cols").grid(row=0, column=2)
        ttk.Entry(size_row, textvariable=self.cols_var, width=5).grid(row=0, column=3, padx=4)
        ttk.Button(panel, text="Apply Grid Size", command=self.apply_grid_size).pack(fill="x")

        ttk.Separator(panel).pack(fill="x", pady=8)

        ttk.Label(panel, text="Click mode", font=("", 10, "bold")).pack(anchor="w")
        for label, val in [("Place / Remove Wall", "wall"),
                            ("Set Start", "start"),
                            ("Set Goal", "goal")]:
            ttk.Radiobutton(panel, text=label, value=val, variable=self.click_mode).pack(anchor="w")

        ttk.Separator(panel).pack(fill="x", pady=8)

        ttk.Label(panel, text="Random maze", font=("", 10, "bold")).pack(anchor="w")
        dens_row = ttk.Frame(panel)
        dens_row.pack(anchor="w", pady=(0, 4))
        ttk.Label(dens_row, text="Density %").pack(side="left")
        self.density_var = tk.IntVar(value=30)
        ttk.Entry(dens_row, textvariable=self.density_var, width=5).pack(side="left", padx=4)
        ttk.Button(panel, text="Generate Random Maze", command=self.random_maze).pack(fill="x")
        ttk.Button(panel, text="Clear Walls", command=self.clear_walls).pack(fill="x", pady=(2, 0))

        ttk.Separator(panel).pack(fill="x", pady=8)

        ttk.Label(panel, text="Algorithm", font=("", 10, "bold")).pack(anchor="w")
        self.algo_var = tk.StringVar(value="A*")
        ttk.Combobox(panel, textvariable=self.algo_var, state="readonly",
                     values=list(ALGORITHMS.keys())).pack(fill="x")

        ttk.Label(panel, text="Heuristic (GBFS / A*)", font=("", 10, "bold")).pack(anchor="w", pady=(8, 0))
        self.heur_var = tk.StringVar(value="Manhattan")
        ttk.Combobox(panel, textvariable=self.heur_var, state="readonly",
                     values=list(HEURISTICS.keys())).pack(fill="x")

        ttk.Separator(panel).pack(fill="x", pady=8)

        ttk.Button(panel, text="Run Search", command=self.run_search).pack(fill="x")
        ttk.Button(panel, text="Reset Visualization", command=self.reset_visualization).pack(fill="x", pady=(2, 0))

        ttk.Separator(panel).pack(fill="x", pady=8)

        ttk.Label(panel, text="Metrics", font=("", 10, "bold")).pack(anchor="w")
        self.metrics_var = tk.StringVar(value="Nodes Expanded: -\nPath Cost: -\nExecution Time: - ms")
        ttk.Label(panel, textvariable=self.metrics_var, justify="left").pack(anchor="w")

    def _build_canvas(self):
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.grid(row=0, column=1, sticky="nsew")
        self.canvas.bind("<Button-1>", self.on_click)

    def apply_grid_size(self):
        try:
            r, c = int(self.rows_var.get()), int(self.cols_var.get())
            if r < 3 or c < 3 or r > 30 or c > 30:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid size", "Rows/Cols must be integers >= 3 and <=30")
            return
        self.rows, self.cols = r, c
        self.grid = [[0] * self.cols for _ in range(self.rows)]
        self.start = (0, 0)
        self.goal = (self.rows - 1, self.cols - 1)
        self.draw_grid()

    def random_maze(self):
        density = max(0, min(100, int(self.density_var.get()))) / 100.0
        self.grid = generate_random_grid(self.rows, self.cols, density, self.start, self.goal)
        self.draw_grid()

    def clear_walls(self):
        self.grid = [[0] * self.cols for _ in range(self.rows)]
        self.draw_grid()

    def reset_visualization(self):
        self.draw_grid()
        self.metrics_var.set("Nodes Expanded: -\nPath Cost: -\nExecution Time: - ms")

    def draw_grid(self, overlay=None):
        """overlay: optional dict {(r,c): 'frontier'|'visited'|'path'} drawn on top of base grid"""
        overlay = overlay or {}
        self.canvas.delete("all")
        self.canvas.config(width=self.cols * CELL_SIZE, height=self.rows * CELL_SIZE)
        for r in range(self.rows):
            for c in range(self.cols):
                x0, y0 = c * CELL_SIZE, r * CELL_SIZE
                x1, y1 = x0 + CELL_SIZE, y0 + CELL_SIZE
                if (r, c) == self.start:
                    color = COLORS["start"]
                elif (r, c) == self.goal:
                    color = COLORS["goal"]
                elif (r, c) in overlay:
                    color = COLORS[overlay[(r, c)]]
                elif self.grid[r][c] == 1:
                    color = COLORS["wall"]
                else:
                    color = COLORS["empty"]
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=COLORS["grid_line"])

    def on_click(self, event):
        c, r = event.x // CELL_SIZE, event.y // CELL_SIZE
        if not (0 <= r < self.rows and 0 <= c < self.cols):
            return
        mode = self.click_mode.get()
        if mode == "start":
            if (r, c) != self.goal:
                self.start = (r, c)
        elif mode == "goal":
            if (r, c) != self.start:
                self.goal = (r, c)
        else:  # wall toggle
            if (r, c) not in (self.start, self.goal):
                self.grid[r][c] = 0 if self.grid[r][c] == 1 else 1
        self.draw_grid()

    def run_search(self):
        algo_name = self.algo_var.get()
        heuristic_fn = HEURISTICS[self.heur_var.get()]
        result = ALGORITHMS[algo_name](self.grid, self.start, self.goal, heuristic_fn)
        self._animate(result)

    def _animate(self, result):
        events = result["events"]
        overlay = {}

        def step(i=0):
            if i < len(events):
                kind, node = events[i]
                if node not in (self.start, self.goal):
                    overlay[node] = kind
                self.draw_grid(overlay)
                self.root.after(ANIMATION_DELAY_MS, step, i + 1)
            else:
                # draw final path on top
                if result["path"]:
                    for node in result["path"]:
                        if node not in (self.start, self.goal):
                            overlay[node] = "path"
                    self.draw_grid(overlay)
                cost_txt = result["cost"] if result["cost"] is not None else "No path found"
                self.metrics_var.set(
                    f"Nodes Expanded: {result['expanded']}\n"
                    f"Path Cost: {cost_txt}\n"
                    f"Execution Time: {result['time_ms']:.3f} ms"
                )

        step()


if __name__ == "__main__":
    root = tk.Tk()
    app = PathfinderApp(root)
    root.mainloop()
