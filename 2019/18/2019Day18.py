"""Advent of Code - Day 18, Year 2019
Solution Started: Jan 30, 2025
Puzzle Link: https://adventofcode.com/2019/day/18
Solution by: abbasmoosajee07
Brief: [Breaking a Vault]
"""

#!/usr/bin/env python3
import os, time

# Main execution
start_time = time.time()

# Define the file paths for input
D18_file = "Day18_input.txt"
D18_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D18_file)

with open(D18_file_path) as file:
    input_data = file.read().strip().split('\n')

class TritonVault:
    KEYS = "abcdefghijklmnopqrstuvwxyz"
    DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Left, Right, Up, Down

    def __init__(self, init_grid: list[str]):
        self.init_grid = init_grid

    def bfs_distances(self, source, vault):
        """
        Perform BFS from a given source point to all reachable points of interest.
        """
        sx, sy = source
        visited = set([(sx, sy)])
        queue = [(sx, sy, 0, "")]
        route_info = {}

        while queue:
            x, y, dist, route = queue.pop(0)
            contents = vault[y][x]

            if contents not in ".@1234#" and dist > 0:
                route_info[contents] = (dist, route)
                route += contents

            visited.add((x, y))

            for dx, dy in self.DIRECTIONS:
                new_x, new_y = x + dx, y + dy
                if vault[new_y][new_x] != '#' and (new_x, new_y) not in visited:
                    queue.append((new_x, new_y, dist + 1, route))

        return route_info

    def find_routes(self, vault):
        """
        Find route information for all points of interest in the grid.
        """
        route_info = {}
        for y in range(len(vault)):
            for x in range(len(vault[y])):
                content = vault[y][x]
                if content in self.KEYS + "@1234":
                    route_info[content] = self.bfs_distances((x, y), vault)
        return route_info

    def divide_vault(self, full_vault):
        """
        Modify the vault by splitting it into four quadrants.
        """
        full_vault = [list(row) for row in full_vault]
        x, y = len(full_vault[0]) // 2, len(full_vault) // 2
        for dx, dy in [(0, 0), (1, 0), (0, 1), (-1, 0), (0, -1)]:
            full_vault[y + dy][x + dx] = '#'
        full_vault[y - 1][x - 1] = '1'
        full_vault[y - 1][x + 1] = '2'
        full_vault[y + 1][x - 1] = '3'
        full_vault[y + 1][x + 1] = '4'
        return ["".join(row) for row in full_vault]

    def run_single_bot(self):
        """
        Finding the shortest path to collect all keys.
        """
        route_info = self.find_routes(self.init_grid)
        keys = frozenset(k for k in route_info.keys() if k in self.KEYS)

        state_info = {('@', frozenset()): 0}

        for _ in range(len(keys)):
            next_state_info = {}

            for (cur_loc, cur_keys), cur_dist in state_info.items():
                for new_key in keys:
                    if new_key not in cur_keys:
                        dist, route = route_info[cur_loc][new_key]
                        reachable = all(c in cur_keys or c.lower() in cur_keys for c in route)

                        if reachable:
                            new_dist = cur_dist + dist
                            new_keys = frozenset(cur_keys | {new_key})

                            if (new_key, new_keys) not in next_state_info or new_dist < next_state_info[(new_key, new_keys)]:
                                next_state_info[(new_key, new_keys)] = new_dist

            state_info = next_state_info
        return min(state_info.values())

    def run_multiple_bots(self):
        """
        Finding the shortest path to collect all keys with four robots.
        """
        split_vault = self.divide_vault(self.init_grid)
        route_info = self.find_routes(split_vault)
        keys = frozenset(k for k in route_info.keys() if k in self.KEYS)

        state_info = {(('1', '2', '3', '4'), frozenset()): 0}

        for _ in range(len(keys)):
            next_state_info = {}

            for (cur_locs, cur_keys), cur_dist in state_info.items():
                for new_key in keys:
                    if new_key not in cur_keys:
                        for robot_idx in range(4):
                            if new_key in route_info[cur_locs[robot_idx]]:
                                dist, route = route_info[cur_locs[robot_idx]][new_key]
                                reachable = all(c in cur_keys or c.lower() in cur_keys for c in route)

                                if reachable:
                                    new_dist = cur_dist + dist
                                    new_keys = frozenset(cur_keys | {new_key})
                                    new_locs = list(cur_locs)
                                    new_locs[robot_idx] = new_key
                                    new_locs = tuple(new_locs)

                                    if (new_locs, new_keys) not in next_state_info or new_dist < next_state_info[(new_locs, new_keys)]:
                                        next_state_info[(new_locs, new_keys)] = new_dist

            state_info = next_state_info

        return min(state_info.values())

vault = TritonVault(input_data)

single_bot = vault.run_single_bot()
print("Part 1:", single_bot)
# print(f"Execution Time Part 1: {time.time() - start_time:.5f}")

start_time_part_2 = time.time()
multiple_bots = vault.run_multiple_bots()
print("Part 2:", multiple_bots)
# print(f"Execution Time Part 2: {time.time() - start_time_part_2:.5f}")

# print(f"Execution Time Total: {time.time() - start_time:.5f}")
