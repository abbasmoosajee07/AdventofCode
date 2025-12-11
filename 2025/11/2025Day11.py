"""Advent of Code - Day 11, Year 2025
Solution Started: December 11, 2025
Puzzle Link: https://adventofcode.com/2025/day/11
Solution by: Abbas Moosajee
Brief: [Reactor]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict, deque
from functools import cache

# Load input file
input_file = "Day11_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().splitlines()

class AOC_Reactor:
    def __init__(self, inp_data):
        self.inp_data = inp_data
        self.data_dict = defaultdict(list)
        for line in inp_data:
            device, outputs = line.split(":")
            self.data_dict[device] = outputs.split()

    def build_path_bfs(self, start = "you", target = "out", must_contain = []):
        queue = deque([[start]])
        total_paths = []
        visited = set()
        count = 0
        while queue:
            current_path = queue.popleft()
            last_pos = current_path[-1]
            count += 1

            if last_pos == target and all(req in current_path for req in must_contain):
                total_paths.append(current_path)
                
                # print(current_path)
                continue
            if count % 10000 == 0:
                print(count, len(queue), len(total_paths))

            state = tuple(current_path)
            if state in visited:
                continue
            visited.add(state)

            for next_pos in self.data_dict.get(last_pos, []):
                queue.appendleft(current_path + [next_pos])
        return len(total_paths)

    def count_paths(self, start_node, target, must_contain):

        # state = bitmask of visited required nodes
        req_index = {node: i for i, node in enumerate(must_contain)}
        full_mask = (1 << len(must_contain)) - 1

        @cache
        def dfs(node, mask):
            # If this node is required, set its bit
            if node in req_index:
                mask |= 1 << req_index[node]

            # If we reached target:
            if node == target:
                return {
                    0: 0, 1: 0, 2: 0,
                    3: 1 if mask == full_mask else 0
                }

            # initialize path counts like your template
            paths = {i: 0 for i in range(4)}

            # explore neighbors
            for nxt in self.data_dict[node]:
                sub = dfs(nxt, mask)
                for st, val in sub.items():
                    paths[st] += val
            return paths

        result = dfs(start_node, 0)
        return result[3]     # paths that reached target with full mask

reactor = AOC_Reactor(data)
print("AOC Day 11, P1:", reactor.build_path_bfs())
print("AOC Day 11, P2:", reactor.count_paths(start_node="svr", target="out", must_contain=["dac", "fft"]))
