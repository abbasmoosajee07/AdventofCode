"""Advent of Code - Day 5, Year 2025
Solution Started: December 5, 2025
Puzzle Link: https://adventofcode.com/2025/day/5
Solution by: Abbas Moosajee
Brief: [Cafeteria]"""

#!/usr/bin/env python3
from pathlib import Path

# Load input file
input_file = "Day05_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read().split("\n\n")

class AOC_Cafeteria:
    def __init__(self, inp_data):
        self.fresh_range = [tuple(map(int, id_range.split("-"))) for id_range in data[0].split("\n")]
        self.ingredients = list(map(int, data[1].split("\n")))

    def check_freshness(self, ingr):
        for start, end in self.fresh_range:
            if start <= ingr <= end:
                return True
        return False

    def count_fresh_ingredients(self):
        fresh_count = 0
        for check_ing in self.ingredients:
            fresh = self.check_freshness(check_ing)
            if fresh:
                fresh_count += 1
        return fresh_count

    def count_total(self):
        sorted_range = sorted(self.fresh_range, key=lambda x: x[0])

        merged_range = []
        current_start, current_end = sorted_range[0]

        for start, end in sorted_range[1:]:
            if start <= current_end + 1:
                current_end = max(current_end, end)
            else:
                merged_range.append((current_start, current_end))
                current_start, current_end = start, end

        merged_range.append((current_start, current_end))

        total = 0
        for start, end in merged_range:
            total += (end - start) + 1

        return total

cafe = AOC_Cafeteria(data)

print("AoC Day 05, P1:", cafe.count_fresh_ingredients())
print("AoC Day 05, P2:", cafe.count_total())