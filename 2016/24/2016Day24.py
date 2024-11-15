# Advent of Code - Day 24, Year 2016
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2016/day/24
# Solution by: [abbasmoosajee07]
# Brief: [Shortest path problem with multiple points]

import os
import numpy as np
from collections import deque
from itertools import permutations

D24_file = 'Day24_input.txt'
D24_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D24_file)

with open(D24_file_path) as file:
    input = file.read().splitlines()

def find_interest_points(grid):
    numbers = []
    for row_idx, row in enumerate(grid):
        for col_idx, char in enumerate(row):
            if char.isdigit():
                numbers.append((int(char), (row_idx, col_idx)))
    return numbers

def breadth_find_search(grid, start, goal):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    rows, cols = len(grid), len(grid[0])
    queue = deque([(start[0], start[1], 0)])  # (row, col, distance)
    visited = set()
    visited.add((start[0], start[1]))

    while queue:
        r, c, dist = queue.popleft()

        if (r, c) == goal:
            return dist

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited:
                if grid[nr][nc] == "." or (nr, nc) == goal:
                    visited.add((nr, nc))
                    queue.append((nr, nc, dist + 1))

    return float('inf')  # Return infinity if no path found

def calculate_distances(grid, points):
    distances = {}
    for i, start in enumerate(points):
        for goal in points[i + 1:]:
            dist = breadth_find_search(grid, start, goal)
            distances[(start, goal)] = dist
            distances[(goal, start)] = dist  # The graph is undirected
    return distances

def find_shortest_path_1(grid, points):
    distances = calculate_distances(grid, points)
    all_permutations = permutations(points)
    shortest_path = float('inf')

    for perm in all_permutations:
        total_distance = 0
        for i in range(len(perm) - 1):
            total_distance += distances.get((perm[i], perm[i + 1]), float('inf'))
            if total_distance >= shortest_path:  # Early exit if we exceed current shortest path
                break
        shortest_path = min(shortest_path, total_distance)

    return shortest_path if shortest_path != float('inf') else -1

def find_shortest_path_2(grid, points):
    n = len(points)
    distances = np.zeros((n, n))  # Initialize distance matrix

    # Calculate distances between every pair of points
    for i in range(n):
        for j in range(n):
            if i != j:
                dist = breadth_find_search(grid, points[i], points[j])
                distances[i][j] = dist
    
    # Dynamic programming for TSP
    dp = [[float('inf')] * n for _ in range(1 << n)]
    dp[1][0] = 0  # Start at the starting point (0) with only 0 visited

    for mask in range(1 << n):
        for u in range(n):
            if not (mask & (1 << u)):
                continue
            for v in range(n):
                if mask & (1 << v):
                    continue
                new_mask = mask | (1 << v)
                dp[new_mask][v] = min(dp[new_mask][v], dp[mask][u] + distances[u][v])
    
    # Return to the starting point (0)
    return min(dp[(1 << n) - 1][v] + distances[v][0] for v in range(n))


numbers = find_interest_points(input)

# # Output the list of found numbers with their coordinates
# for number, (row, col) in numbers:
#     print(f"Found number {number} at position (row {row}, col {col})")

points = [num[1] for num in numbers]
shortest_path_1 = find_shortest_path_1(input, points)
print(f"Part 1: Fewest Steps to meet all points: {shortest_path_1}")

shortest_path_2 = find_shortest_path_2(input, points)
print(f"Part 2: Fewest Steps to meet all points: {shortest_path_2}")
