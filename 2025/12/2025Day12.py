"""Advent of Code - Day 12, Year 2025
Solution Started: December 12, 2025
Puzzle Link: https://adventofcode.com/2025/day/12
Solution by: Abbas Moosajee
Brief: [Christmas Tree Farm]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import defaultdict
from math import prod

# Load input file
input_file = "Day12_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().split("\n\n")

class AOC_Farm:
    def __init__(self, input_text):
        self.shape_counts = {}
        self.regions = []

        for grouped_data in input_text:
            if "#" in grouped_data:
                grouped_data = grouped_data.split("\n")
                index_no = int(grouped_data[0].strip(":"))
                present_shape = [list(row) for row in grouped_data[1:]]
                self.shape_counts[index_no] = sum(row.count('#') for row in present_shape)
            else:
                for regiod_data in grouped_data.split("\n"):
                    region_size, presents_needed = regiod_data.split(":")
                    presents_needed = tuple(map(int, presents_needed.split()))
                    region_size = tuple(map(int, region_size.split("x")))
                    self.regions.append((region_size, presents_needed))

    def fit_all_presents(self) -> int:
        total_presents = 0
        for region_size, num_shapes in self.regions:
            needed = sum(self.shape_counts[id] * n for id, n in enumerate(num_shapes))
            if prod(region_size) >= needed:
                total_presents += 1
        return total_presents

print("AOC Day 12, P1:", AOC_Farm(data).fit_all_presents())
