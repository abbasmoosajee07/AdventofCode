# Advent of Code - Day 3, Year 2017
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2017/day/3
# Solution by: [abbasmoosajee07]
# Brief: [Spiral number grids]

import os
import numpy as np
from collections import deque
from itertools import count

D3_file = 'Day03_input.txt'
D3_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D3_file)

with open(D3_file_path) as file:
    input = file.read()

def spiral_cw(A):
    """Extracts elements from a 2D array in clockwise spiral order."""
    A = np.array(A)
    out = []
    while A.size:
        out.append(A[0])        # Take the first row
        A = A[1:].T[::-1]       # Cut off the first row and rotate counterclockwise
    return np.concatenate(out)

def spiral_ccw(A):
    """Extracts elements from a 2D array in counterclockwise spiral order."""
    A = np.array(A)
    out = []
    while A.size:
        out.append(A[0][::-1])  # First row reversed
        A = A[1:][::-1].T       # Cut off first row and rotate clockwise
    return np.concatenate(out)

def base_spiral(nrow, ncol):
    """Generates the base spiral index for a 2D grid."""
    return spiral_ccw(np.arange(nrow * ncol).reshape(nrow, ncol))[::-1]

def to_spiral(A):
    """Converts a 2D array into a spiral form."""
    A = np.array(A)
    B = np.empty_like(A)
    B.flat[base_spiral(*A.shape)] = A.flat
    return B[::-1]

def from_spiral(A):
    """Converts a spiral array back into its original form."""
    A = np.array(A)
    return A.flat[base_spiral(*A.shape)].reshape(A.shape)

def bfs(grid, start, goal, ignore_values=False):
    """Performs BFS on a grid to find the shortest path from start to goal."""
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    rows, cols = len(grid), len(grid[0])
    queue = deque([(start[0], start[1], 0)])  # (row, col, distance)
    visited = {start}

    while queue:
        r, c, dist = queue.popleft()
        if (r, c) == goal:
            return dist

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                if ignore_values or grid[nr][nc] == 0:
                    visited.add((nr, nc))
                    queue.append((nr, nc, dist + 1))

    return -1

def sum_spiral():
    """Generates the sum of neighbors in a spiral pattern."""
    a, i, j = {(0, 0): 1}, 0, 0
    for s in count(1, 2):
        for (ds, di, dj) in [(0, 1, 0), (0, 0, -1), (1, -1, 0), (1, 0, 1)]:
            for _ in range(s + ds):
                i += di
                j += dj
                a[i, j] = sum(a.get((k, l), 0) for k in range(i-1, i+2) for l in range(j-1, j+2))
                yield a[i, j]

def find_next_value(n):
    """Finds the first value in the spiral that exceeds n."""
    for x in sum_spiral():
        if x > n:
            return x

# Example usage for Part 1
input_value = int(input)
grid_size = int(np.ceil(np.sqrt(input_value)))
grid = np.arange(1, (grid_size ** 2) + 1).reshape(grid_size, grid_size)
spiralled_grid = to_spiral(grid)

# Get starting and goal positions
start = tuple(np.argwhere(spiralled_grid == input_value).flatten())
goal = tuple(np.argwhere(spiralled_grid == 1).flatten())

# Find shortest path using BFS
shortest_path_length = bfs(spiralled_grid, start, goal, ignore_values=True)

if shortest_path_length != -1:
    print(f"The shortest path from {input_value} at {start} to 1 at {goal} is {shortest_path_length} steps.")
else:
    print(f"No path found from {start} to {goal}.")

# Example usage for Part 2
P2_next_val = find_next_value(input_value)
print(f"Part 2: The next value in the grid spiral exceeding {input_value} is: {P2_next_val}")
