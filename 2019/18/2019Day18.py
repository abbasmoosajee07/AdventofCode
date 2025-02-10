"""Advent of Code - Day 18, Year 2019
Solution Started: Jan 30, 2025
Puzzle Link: https://adventofcode.com/2019/day/18
Solution by: abbasmoosajee07
Brief: [Breaking a Vault]
"""

#!/usr/bin/env python3
import os, time
import networkx as nx
from itertools import combinations
from collections import defaultdict, deque

# Define the file paths for input
D18_file = "Day18_input.txt"
D18_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D18_file)

with open(D18_file_path) as file:
    input_data = file.read().strip().split('\n')

class Path:
    """
    Represents a path in the maze, tracking current position, collected keys, and path length.
    """
    def __init__(self, current, collected_keys, length):
        self.current = current  # Current positions in the maze
        self.collected_keys = collected_keys  # Collected keys as a bitmask
        self.length = length  # Length of the current path

    def get_state(self):
        """Return the current state as a tuple of position and collected keys."""
        return (self.current, self.collected_keys)

    def path_length(self):
        """Return the number of collected keys based on the bitmask."""
        return bin(self.collected_keys).count("1")

    def __repr__(self):
        """String representation of the path."""
        return f"{self.current} {bin(self.collected_keys)} : {self.length}"


class TritonVault:
    """
    Represents the vault with keys, doors, and the maze grid.
    """
    PATH_MARKER = '█' if '█'.encode().decode('utf-8', 'ignore') else '|'  # Marker for path visualization

    def __init__(self, init_grid):
        self.init_grid = init_grid  # The initial grid of the vault

    def load_grid(self):
        """Parse the initial grid to extract keys, doors, and other relevant information."""
        grid = defaultdict(int)
        keys, doors, start_points, base_grid = {}, {}, [], {}

        for y, line in enumerate(self.init_grid):
            for x, cell in enumerate(line):
                base_grid[(x, y)] = cell
                if cell != '#':  # Ignore walls
                    p = {'x': x, 'y': y}
                    grid[(x, y)] = 1
                    if cell == '@':  # Start points
                        start_points.append(p)
                    elif cell.islower():  # Keys
                        keys[ord(cell) - 97] = p
                    elif cell.isupper():  # Doors
                        doors[ord(cell) - 65] = p

        self.doors = doors
        self.keys = keys
        self.grid_size = (len(self.init_grid[0]) - 1, len(self.init_grid) - 1)
        self.BASE_GRID = base_grid
        self.grid = grid
        self.start_points = start_points

        return self.grid, self.start_points

    def divide_vault(self, base_vault: dict):
        """Divide the vault into sections and adjust grid and starting points."""
        mid_row, mid_col = self.start_points[0].values()
        all_robots = []
        corrected_grid = base_vault
        corrections = {(-1, -1): '@', (-1, 0): '#', (-1, 1): '@',
                       (0, -1): '#', (0, 0): '#', (0, 1): '#',
                       (1, -1): '@', (1, 0): '#', (1, 1): '@'}

        for (dr, dc), new_tile in corrections.items():
            x, y = (mid_row + dr, mid_col + dc)
            corrected_grid[(x, y)] = new_tile
            self.grid[(x, y)] = 1 if new_tile != '#' else 0
            if new_tile == '@':
                new_pos = {'x': x, 'y': y}
                all_robots.append(new_pos)

        self.BASE_GRID = corrected_grid
        self.start_points = all_robots

        return self.grid, all_robots

    @staticmethod
    def get_surrounding_points(p):
        """Get the surrounding points (up, down, left, right) for a given point."""
        x, y = p['x'], p['y']
        return {(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)}

    @staticmethod
    def build_graph(grid, max_x, max_y):
        """Build a graph from the grid, with edges between walkable points."""
        edges = []
        for x in range(max_x + 1):
            for y in range(max_y + 1):
                p = (x, y)
                if grid[p]:
                    for sp in TritonVault.get_surrounding_points({'x': x, 'y': y}):
                        if grid[sp]:
                            edges.append((p, sp))
        return nx.Graph(edges)

    @staticmethod
    def compute_key_distances(G, keys, doors, start_points, start_points_nums):
        """Compute distances between keys and starting points, considering doors."""
        def get_distance(p0, p1, doors):
            """Calculate the distance between two points, considering doors."""
            if not nx.has_path(G, tuple(p0.values()), tuple(p1.values())):
                return None
            path = nx.shortest_path(G, tuple(p0.values()), tuple(p1.values()))
            path_set = set(path)
            doors_in_way = 0
            for k, p in doors.items():
                if tuple(p.values()) in path_set:
                    doors_in_way |= (1 << k)
            return len(path) - 1, doors_in_way

        key_to_key = defaultdict(dict)
        key_to_bits = {k: 1 << k for k in keys.keys()}

        for start_point, start_point_num in zip(start_points, start_points_nums):
            start_point_bits = 1 << start_point_num
            for k, p in keys.items():
                k_bits = key_to_bits[k]
                res = get_distance(start_point, p, doors)
                if res:
                    distance, doors_in_way = res
                    key_to_key[start_point_bits][k_bits] = (distance, doors_in_way)

        for k0, k1 in combinations(keys.keys(), 2):
            k0_bits = key_to_bits[k0]
            k1_bits = key_to_bits[k1]
            res = get_distance(keys[k0], keys[k1], doors)
            if res:
                distance, doors_in_way = res
                key_to_key[k0_bits][k1_bits] = (distance, doors_in_way)
                key_to_key[k1_bits][k0_bits] = (distance, doors_in_way)

        return dict(key_to_key)

    @staticmethod
    def find_next_possible_paths(key_to_key, path, total_keys):
        """Find the next possible paths from the current position and collected keys."""
        current_positions = path.current
        for k0, v0 in key_to_key.items():
            if k0 & current_positions:
                for k1, v1 in v0.items():
                    if not k1 & path.collected_keys:
                        dist, doors_in_way = v1
                        if doors_in_way & path.collected_keys == doors_in_way:
                            new_position = current_positions ^ k0 | k1
                            yield Path(new_position, path.collected_keys | k1, path.length + dist)

    def print_maze(self, path_taken: dict = {}):
        """
        Display the maze with path visualization.
        """
        grid = self.BASE_GRID
        min_row = min(y for x, y in grid)
        max_row = max(y for x, y in grid)
        min_col = min(x for x, y in grid)
        max_col = max(x for x, y in grid)

        vault_grid = []
        for row_no in range(min_row, max_row + 1):
            row = ''
            for col_no in range(min_col, max_col + 1):
                pos = (col_no, row_no)
                if pos in path_taken:
                    tile = self.PATH_MARKER  # Path visualization
                elif pos in grid:
                    tile = grid[pos]
                row += tile
            vault_grid.append(row)

        print("\n".join(vault_grid))
        print("_" * (max_col - min_col + 1))

    def find_smallest_path(self, grid: dict, start_points: list, visualize: bool = False):
        """
        Find the smallest path that collects all keys in the vault.
        """
        max_x, max_y = self.grid_size
        total_start_points = len(start_points)
        keys = {k + total_start_points: v for k, v in self.keys.items()}
        doors = {k + total_start_points: v for k, v in self.doors.items()}
        G = self.build_graph(grid, max_x, max_y)

        total_keys = len(keys)
        start_points_nums = list(range(len(start_points)))
        start_points_bits = sum(1 << num for num in start_points_nums)

        key_to_key = self.compute_key_distances(G, keys, doors, start_points, start_points_nums)
        start_path = Path(start_points_bits, 0, 0)

        min_full_path_length = float('inf')
        min_path_lengths = defaultdict(int)

        counter = 0
        possible_paths = deque([start_path])
        while possible_paths:
            counter += 1
            path = possible_paths.popleft()

            if min_path_lengths[path.get_state()] < path.length:
                continue

            for new_path in self.find_next_possible_paths(key_to_key, path, total_keys):
                if new_path.length < min_full_path_length:
                    unique_state = new_path.get_state()
                    if unique_state in min_path_lengths and new_path.length >= min_path_lengths[unique_state]:
                        continue

                    min_path_lengths[unique_state] = new_path.length

                    if new_path.path_length() == total_keys:
                        min_full_path_length = min(min_full_path_length, new_path.length)
                    else:
                        possible_paths.append(new_path)

        return min_full_path_length

# Main execution
start_time = time.time()
vault = TritonVault(input_data)

base_vault, single_bot = vault.load_grid()
path_p1 = vault.find_smallest_path(base_vault, single_bot)
print("Part 1:", path_p1)
# print(f"Execution Time Part 1: {time.time() - start_time:.5f}")

start_time_part_2 = time.time()
split_vault, all_bots = vault.divide_vault(vault.BASE_GRID)
path_p2 = vault.find_smallest_path(split_vault, all_bots)
print("Part 2:", path_p2)
# print(f"Execution Time Part 2: {time.time() - start_time_part_2:.5f}")
# print(f"Execution Time Total: {time.time() - start_time:.5f}")
