"""Advent of Code - Day 2, Year 2025
Solution Started: December 2, 2025
Puzzle Link: https://adventofcode.com/2025/day/2
Solution by: Abbas Moosajee
Brief: [Gift Shop]"""

#!/usr/bin/env python3
from pathlib import Path
from collections import Counter
# Load input file
input_file = "Day02_input.txt"
input_path = Path(__file__).parent / input_file

with input_path.open("r", encoding="utf-8") as f:
    data = f.read()

def count_invalid_ids_p1(product_range):
    invalid_ids = set()
    for id_range in product_range.split(","):
        id_start, id_end = id_range.split("-")
        for test_id in range(int(id_start), int(id_end) + 1):
            id_str = str(test_id)
            id_half = len(id_str) // 2
            if id_str[:id_half] == id_str[id_half:]:
                invalid_ids.add(test_id)
                break
    return sum(invalid_ids)

def count_invalid_ids_p2(product_range):
    invalid_ids = set()
    for id_range in product_range.split(","):
        id_start, id_end = id_range.split("-")
        for test_id in range(int(id_start), int(id_end) + 1):
            id_str = str(test_id)
            id_len = len(id_str)
            for pattern_len in range(1, id_len):
                pattern = id_str[:pattern_len]
                if id_str.count(pattern) * pattern_len == id_len:
                    invalid_ids.add(test_id)
                    break
    return sum(invalid_ids)

print("AoC Day 2, P1:", count_invalid_ids_p1(data))
print("AoC Day 2, P2:", count_invalid_ids_p2(data))
