"""Advent of Code - Day 8, Year 2024
Solution Started: Dec 8, 2024
Puzzle Link: https://adventofcode.com/2024/day/8
Solution by: abbasmoosajee07
Brief: [Antennas]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

# Load the input data from the specified file path
D08_file = "Day08_input.txt"
D08_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D08_file)

# Read and sort input data into a grid
with open(D08_file_path) as file:
    input_data = file.read().strip().split('\n')
    antenna_map = np.array([list(row) for row in input_data])

def find_antennas(map):
    antenna_list = defaultdict(list)
    rows, cols = map.shape
    for r in range(rows):
        for c in range(cols):
            pos = (r,c)
            if map[pos] != '.':
                antenna_list[map[pos]].append((pos))
    return antenna_list

R, C = antenna_map.shape

antenna_list = find_antennas(antenna_map)

antinodes_p1 = set()
antinodes_p2 = set()
for r in range(R):
    for c in range(C):
        for freq, coordinate_list in antenna_list.items():
            for (r1,c1) in coordinate_list:
                for (r2,c2) in coordinate_list:
                    if (r1,c1) != (r2,c2):
                            abs_d1 = abs(r-r1) + abs(c-c1)
                            abs_d2 = abs(r-r2) + abs(c-c2)

                            dr1, dr2 = r-r1, r-r2
                            dc1, dc2 = c-c1, c-c2

                            if 0<=r<R and 0<=c<C and (dr1*dc2 == dc1*dr2):
                                # print(f' {c=} {r1=} {c1=} {r2=} {c2=} {k=} {dr1=} {dr2=} {dc1=} {dc2=}')
                                antinodes_p2.add((r,c))
                                if (abs_d1==2*abs_d2 or abs_d1*2==abs_d2):
                                    antinodes_p1.add((r,c))

print("Part 1:", len(antinodes_p1))
print("Part 2:", len(antinodes_p2))

