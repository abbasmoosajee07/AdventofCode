"""Advent of Code - Day 18, Year 2019
Solution Started: Jan 30, 2025
Puzzle Link: https://adventofcode.com/2019/day/18
Solution by: abbasmoosajee07
Brief: [Breaking a Vault, with Visualisation]
"""

#!/usr/bin/env python3
import os, time, heapq
from collections import deque

# Define the file paths for input
D18_file = "Day18_input.txt"
D18_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D18_file)

with open(D18_file_path) as file:
    input_data = file.read().strip().split('\n')

start_time = time.time()

class TritonVault:
    def __init__(self, blueprints: list[str]):
        self.blueprint = blueprints
        self.path_marker = '█' if '█'.encode().decode('utf-8', 'ignore') else '|'
        self.DIRECTIONS = {'<': (0, -1), '>': (0, 1), '^': (-1, 0), 'v': (1, 0)}

        # Initialize grid attributes
        self.init_robot = None
        self.passage = set()
        self.WALLS = set()
        self.DOORS_KEYS = dict()
        self.BASE_VAULT = dict()
        self.parse_grid(blueprints)

    def parse_grid(self, vault: list[str] = None):
        """
        Parse the grid from blueprint and identify special elements.
        """
        vault = vault or self.blueprint

        for row_no, row in enumerate(vault):
            for col_no, tile in enumerate(row):
                pos = (row_no, col_no)
                self.BASE_VAULT[pos] = tile

                if tile == '@':  # Starting position
                    self.init_robot = pos

                elif tile == '#':  # Wall
                    self.WALLS.add(pos)

                elif tile == '.':  # Passage
                    self.passage.add(pos)

                else:  # Doors or Keys
                    self.DOORS_KEYS[tile] = pos

    def get_next_position(self, init_pos: tuple[int, int], move: str) -> tuple[int, int]:
        """
        Return the next position based on the current position and direction.
        """
        dr, dc = self.DIRECTIONS[move]
        return init_pos[0] + dr, init_pos[1] + dc

    def print_maze(self, path_taken: dict = {}, base_grid: dict = {}):
        """
        Display the maze with path visualization.
        """
        grid_dict = base_grid or self.BASE_VAULT
        coords_set = set(grid_dict.keys())
        min_row = min(row for row, _ in coords_set)
        max_row = max(row for row, _ in coords_set)
        min_col = min(col for _, col in coords_set)
        max_col = max(col for _, col in coords_set)

        vault_grid = []

        for row_no in range(min_row, max_row + 1):
            row = ''
            for col_no in range(min_col, max_col + 1):
                pos = (row_no, col_no)
                if pos in self.WALLS:
                    tile = '#'
                elif pos in path_taken:
                    tile = path_taken[pos]
                else:
                    tile = self.BASE_VAULT.get(pos, '.')
                row += tile
            vault_grid.append(row)

        print("\n".join(vault_grid))
        print("_" * (max_col - min_col + 1))
        return vault_grid

    def run_single_bot(self, visualize: bool = False) -> int:
        """
        Map and visualize the shortest path from the start to collect all keys using BFS.
        """
        # Initialize BFS queue: (steps, current_pos, collected_keys_bitmask)
        queue = deque([(0, self.init_robot, 0)])

        # Compute the bitmask for all keys
        all_keys_bitmask = (1 << len([k for k in self.DOORS_KEYS if k.islower()])) - 1

        # Visited states to avoid redundant exploration
        visited = set()
        overall_path = {}

        while queue:
            steps, current_pos, collected_keys = queue.popleft()

            # Return if all keys are collected
            if collected_keys == all_keys_bitmask:
                return steps

            # Skip already visited states with the same keys
            state = (current_pos, collected_keys)
            if state in visited:
                continue
            visited.add(state)

            # Explore all adjacent positions
            for direction in self.DIRECTIONS:
                next_pos = self.get_next_position(current_pos, direction)

                # Skip walls
                if next_pos in self.WALLS:
                    continue

                tile = self.BASE_VAULT.get(next_pos, '.')

                # Handle doors
                if tile.isupper() and not (collected_keys & (1 << (ord(tile.lower()) - ord('a')))):
                    continue  # Door is locked, skip this path

                # Handle keys
                new_collected_keys = collected_keys
                if tile.islower():
                    new_collected_keys |= (1 << (ord(tile) - ord('a')))

                # Add the new state to the queue
                queue.append((steps + 1, next_pos, new_collected_keys))
                overall_path[next_pos] = self.path_marker

            if visualize:
                print(f"Move to {next_pos} with steps: {steps + 1}, keys: {bin(new_collected_keys)}")
                self.print_maze(overall_path)

        print("No valid path found.")
        return -1

    def split_vault(self, base_vault: dict):
        mid_row, mid_col = self.init_robot
        all_robots = []
        corrected_grid = base_vault
        corrections = {(-1,-1):'@', (-1,0):'#', (-1,1):'@',
                        (0,-1):'#', (0,0):'#',  (0,1):'#',
                        (1,-1):'@', (1,0):'#', (1,1):'@'}

        for (dr, dc), new_tile in corrections.items():
            new_pos = (mid_row + dr, mid_col + dc)
            corrected_grid[(new_pos)] = new_tile
            if new_tile == '@':
                all_robots.append(new_pos)

        self.SPLIT_VAULT = corrected_grid
        self.all_robots = all_robots

    def run_multiple_bots(self, visualize: bool = False) -> int:
        """
        Optimized solution using memoization and pre-computed paths for multiple bots.
        """

        self.split_vault(self.BASE_VAULT)
        grid_dict = self.SPLIT_VAULT
        allkeys = set(c for c in self.DOORS_KEYS.keys() if c.islower())
        positions = tuple(self.all_robots)

        def reachable_keys(sx, sy, keys):
            """Find all reachable keys from (sx, sy) given collected keys."""
            q = deque([(sx, sy, 0)])
            seen = set()
            reachable = []

            while q:
                cx, cy, steps = q.popleft()
                if (cx, cy) in seen:
                    continue
                seen.add((cx, cy))

                tile = grid_dict.get((cy, cx), '#')
                if tile.islower() and tile not in keys:
                    reachable.append((steps, cx, cy, tile))
                    continue

                if tile == '#' or (tile.isupper() and tile.lower() not in keys):
                    continue

                for dx, dy in self.DIRECTIONS.values():
                    nx, ny = cx + dx, cy + dy
                    q.append((nx, ny, steps + 1))

            return reachable

        # Priority queue stores (steps, positions, collected_keys)
        pq = [(0, positions, frozenset())]
        seen = {}

        while pq:
            steps, current_positions, keys = heapq.heappop(pq)
            # print(steps, current_positions, keys)

            if keys == allkeys:
                return steps

            state_key = (current_positions, keys)
            if state_key in seen and seen[state_key] <= steps:
                continue
            seen[state_key] = steps

            for i, (cx, cy) in enumerate(current_positions):
                for l, nx, ny, key in reachable_keys(cx, cy, keys):
                    new_positions = current_positions[:i] + ((nx, ny),) + current_positions[i + 1:]
                    new_keys = keys | frozenset([key])
                    heapq.heappush(pq, (steps + l, new_positions, new_keys))

        print("No valid path found.")
        return -1


test_data = ['#############','#g#f.D#..h#l#','#F###e#E###.#','#dCba...BcIJ#','#####.@.#####','#nK.L...G...#','#M###N#H###.#','#o#m..#i#jk.#','#############']
test_data = ['#############','#DcBa.#.GhKl#','#.###...#I###','#e#d#.@.#j#k#','###C#...###J#','#fEbA.#.FgHi#','#############']

vault = TritonVault(input_data)
bot_steps = vault.run_single_bot()
print("Part 1:", bot_steps)
print(f"Execution Time: {time.time() - start_time:.5f}")

time2 = time.time()

mult_bots = vault.run_multiple_bots()
print("Part 2:", mult_bots)

print(f"Execution Time: {time.time() - time2:.5f}")
print(f"Execution Time: {time.time() - start_time:.5f}")