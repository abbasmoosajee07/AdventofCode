import os, re, copy
import numpy as np
from collections import deque

D24_file = 'Day24_input.txt'
D24_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D24_file)

with open(D24_file_path) as file:
    input = file.read().splitlines()

def find_interest_points(grid):
    numbers = []
    # Loop over each row and column to find numbers
    for row_idx, row in enumerate(grid):
        for col_idx, char in enumerate(row):
            if char.isdigit():  # Check if the character is a number
                numbers.append((int(char), (row_idx, col_idx)))  # Store the number and its coordinates

    return numbers

numbers = find_interest_points(input)
# Output the list of found numbers with their coordinates
for number, (row, col) in numbers:
    print(f"Found number {number} at position (row {row}, col {col})")

# Function to perform BFS on an unweighted grid
def bfs(grid, start, goal):
    # Define the possible movements (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Get grid dimensions
    rows, cols = len(grid), len(grid[0])
    
    # Initialize queue for BFS with the starting point
    queue = deque([(start[0], start[1], 0)])  # (row, col, distance)
    
    # Keep track of visited cells
    visited = set()
    visited.add((start[0], start[1]))
    
    # Perform BFS
    while queue:
        r, c, dist = queue.popleft()
        
        # If we reached the goal, return the distance
        if (r, c) == goal:
            return dist
        
        # Explore neighbors in all four directions
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited and grid[nr][nc] == 0:
                visited.add((nr, nc))
                queue.append((nr, nc, dist + 1))
    
    # If there's no valid path to the goal
    return -1

# Example grid: 0 = open path, 1 = obstacle
grid = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

# Starting point (top-left) and goal point (bottom-right)
start = (0, 0)
goal = (4, 4)

# Find the shortest path using BFS
shortest_path_length = bfs(grid, start, goal)

if shortest_path_length != -1:
    print(f"The shortest path from {start} to {goal} is {shortest_path_length} steps.")
else:
    print(f"No path found from {start} to {goal}.")


# Function to perform BFS on an unweighted grid
def bfs(grid, start, goal):
    # Define the possible movements (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    # Get grid dimensions
    rows, cols = len(grid), len(grid[0])
    
    # Initialize queue for BFS with the starting point
    queue = deque([(start[0], start[1], 0)])  # (row, col, distance)
    
    # Keep track of visited cells
    visited = set()
    visited.add((start[0], start[1]))
    
    # Perform BFS
    while queue:
        r, c, dist = queue.popleft()
        
        # If we reached the goal, return the distance
        if (r, c) == goal:
            return dist
        
        # Explore neighbors in all four directions
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            # Check if the new position is within bounds, not visited, and is a traversable cell (".")
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited and grid[nr][nc] == ".":
                visited.add((nr, nc))
                queue.append((nr, nc, dist + 1))
    
    # If there's no valid path to the goal
    return -1

# Example grid: "." = open path, "#" = obstacle
grid = [
    [0, "#", ".", ".", "."],
    [".", "#", ".", "#", "."],
    [".", ".", ".", "#", "."],
    [".", "#", "#", "#", "."],
    [".", ".", ".", ".", 1]
]

# Starting point (top-left) and goal point (bottom-right)
start = (0, 0)
goal = (4, 4)

# Find the shortest path using BFS
shortest_path_length = bfs(grid, start, goal)

if shortest_path_length != -1:
    print(f"The shortest path from {start} to {goal} is {shortest_path_length} steps.")
else:
    print(f"No path found from {start} to {goal}.")
