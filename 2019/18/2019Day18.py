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

class Path:
    def __init__(self, current, collected_keys, length):
        self.current = current
        self.collected_keys = collected_keys
        self.length = length

    def get_state(self):
        return (self.current, self.collected_keys)

    def path_length(self):
        return bin(self.collected_keys).count("1")

    def __repr__(self):
        return f"{self.current} {bin(self.collected_keys)} : {self.length}"

class TritonVault:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_grid(self, part_b=False):
        grid = defaultdict(int)
        keys, doors, start_points = {}, {}, []

        with open(self.file_path) as f:
            lines = [list(line.strip()) for line in f.readlines()]
            mid_y, mid_x = (len(lines) - 1) // 2, (len(lines[0]) - 1) // 2
            if part_b:
                lines[mid_y-1][mid_x-1:mid_x+2] = "@#@"
                lines[mid_y][mid_x-1:mid_x+2] = "###"
                lines[mid_y+1][mid_x-1:mid_x+2] = "@#@"

            for y, line in enumerate(lines):
                for x, c in enumerate(line):
                    if c != '#':
                        p = {'x': x, 'y': y}
                        grid[(x, y)] = 1
                        if c == '@':
                            start_points.append(p)
                        elif c != '.':
                            o = ord(c)
                            if o >= 97:
                                keys[o - 97] = p
                            else:
                                doors[o - 65] = p

        total_start_points = len(start_points)
        keys = {k + total_start_points: v for k, v in keys.items()}
        doors = {k + total_start_points: v for k, v in doors.items()}

        return grid, keys, doors, start_points, len(lines[0]) - 1, len(lines) - 1

    @staticmethod
    def get_surrounding_points(p):
        x, y = p['x'], p['y']
        return {(x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)}

    @staticmethod
    def build_graph(grid, max_x, max_y):
        edges = []
        for x in range(max_x + 1):
            for y in range(max_y + 1):
                p = (x, y)
                if grid[p]:
                    for sp in TritonVault.get_surrounding_points({'x': x, 'y': y}):
                        if grid[sp]:
                            edges.append((p, sp))
        return nx.Graph(edges)

    def find_smallest_path(self, grid, keys, doors, start_points, max_x, max_y):
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

        return min_full_path_length, counter

    @staticmethod
    def compute_key_distances(G, keys, doors, start_points, start_points_nums):
        def get_distance(p0, p1, doors):
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
        current_positions = path.current
        for k0, v0 in key_to_key.items():
            if k0 & current_positions:
                for k1, v1 in v0.items():
                    if not k1 & path.collected_keys:
                        dist, doors_in_way = v1
                        if doors_in_way & path.collected_keys == doors_in_way:
                            new_position = current_positions ^ k0 | k1
                            yield Path(new_position, path.collected_keys | k1, path.length + dist)

# Main execution
start_time = time.time()
vault = TritonVault(D18_file_path)

grid, keys, doors, start_points, max_x, max_y = vault.load_grid()
path_p1, _ = vault.find_smallest_path(grid, keys, doors, start_points, max_x, max_y)
print("Part 1:", path_p1)
# print(f"Execution Time: {time.time() - start_time:.5f}")

start_time_part_2 = time.time()
grid, keys, doors, start_points, _, _ = vault.load_grid(part_b=True)
path_p2, _ = vault.find_smallest_path(grid, keys, doors, start_points, max_x, max_y)
print("Part 2:", path_p2)
# print(f"Execution Time Part B: {time.time() - start_time_part_2:.5f}")
# print(f"Execution Time Part B: {time.time() - start_time:.5f}")