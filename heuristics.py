"""
heuristics.py
-------------
Heuristic functions h(n) used by Greedy Best-First Search and A*.

Both heuristics take two (row, col) tuples and estimate the distance
between them. They must be ADMISSIBLE (never overestimate the true
cost) for A* to guarantee an optimal path.
"""

import math


def manhattan(a, b):
    """|dx| + |dy|  -> exact cost on a 4-directional grid (cost=1 per move).
    Admissible and consistent for this grid, so A* with Manhattan is optimal."""
    (r1, c1), (r2, c2) = a, b
    return abs(r1 - r2) + abs(c1 - c2)


def euclidean(a, b):
    """Straight-line distance. Still admissible (it's <= Manhattan distance
    on a grid where you can only move in 4 directions), but it UNDERESTIMATES
    more, so it explores more nodes than Manhattan -> weaker guidance."""
    (r1, c1), (r2, c2) = a, b
    return math.hypot(r1 - r2, c1 - c2)


HEURISTICS = {
    "Manhattan": manhattan,
    "Euclidean": euclidean,
}
