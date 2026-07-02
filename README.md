# Pathfinding Visualizer (BFS / UCS / GBFS / A*)

A Tkinter-based GUI to compare uninformed (BFS, UCS) and informed (GBFS, A*)
search algorithms on a grid.

## Requirements
- Python 3.8+
- Tkinter (bundled with standard Python on Windows/macOS; on Linux install
  with `sudo apt install python3-tk` if missing)

No other dependencies.

## Run
```
python main.py
```

## How to use
1. Set **Rows/Cols** and click **Apply Grid Size** now i added tha rows and columns must be greater than 2 and less than 30 (but u can change it in the main file at main_gird func).
2. Choose a **click mode**: Wall (default), Set Start, or Set Goal, then
   click cells on the grid to place them.
3. Optionally click **Generate Random Maze** with a chosen wall density (%).
4. Pick an **Algorithm** (BFS / UCS / GBFS / A*) and, for GBFS/A*, a
   **Heuristic** (Manhattan / Euclidean).
5. Click **Run Search**. Yellow = frontier, Blue = visited/expanded,
   Green = final path. Metrics (nodes expanded, path cost, execution time)
   appear in the side panel.
6. **Reset Visualization** clears the colors but keeps your walls/start/goal.

## Project structure
```
main.py            GUI: grid rendering, mouse input, animation, metrics
algorithms.py       BFS, UCS, GBFS, A* implementations
heuristics.py        Manhattan and Euclidean heuristic functions
maze_generator.py    Random wall generator with adjustable density
```

## Notes for the report
- All moves are 4-directional with unit cost, so BFS's step-count and UCS's
  path cost always agree.
- Execution time is measured with `time.perf_counter()` around the algorithm
  only, separate from the animation delay, so it reflects real computation
  cost, not rendering speed.
- On open, obstacle-free grids A* can expand almost as many nodes as BFS,
  because many cells share the same f(n) value (ties) near the diagonal
  toward the goal. A* clearly outperforms BFS/UCS on maze-like grids where
  the heuristic can rule out large regions early — good material for a
  best-case vs. worst-case comparison in the report.
