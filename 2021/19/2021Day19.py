# Advent of Code - Day 19, Year 2021
# Solution Started: Nov 25, 2024
# Puzzle Link: https://adventofcode.com/2021/day/19
# Solution by: [abbasmoosajee07]
# Brief: [Satellite alignments]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D19_file = "Day19_input.txt"
D19_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D19_file)

# Read and sort input data into a grid
with open(D19_file_path) as file:
    input_data = file.read().strip().split('\n\n')

def parse_scanner_info(input):
    scanner_dict = {}
    for scanner in input:
        split_lines = scanner.split('\n')
        scanner_no = int(re.search(r"\d+", split_lines[0]).group())
        scanner_lines = split_lines[1:]
        scanner_data = [tuple(int(num) for num in row.split(','))
                            for row in scanner_lines]
        scanner_dict[scanner_no] = (scanner_data)
    return scanner_dict

scanner_dict = parse_scanner_info(input_data)
# Define all possible rotations in 3D space (24 orientations)
def generate_rotations():
    """Generate all 24 valid rotations in 3D space."""
    rotations = []
    for perm in [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]:
        for signs in [(1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1),
                      (-1, 1, 1), (-1, 1, -1), (-1, -1, 1), (-1, -1, -1)]:
            rotations.append((perm, signs))
    return rotations


def apply_rotation(coord, rotation):
    """Apply a given rotation to a 3D coordinate."""
    perm, signs = rotation
    return tuple(signs[i] * coord[perm[i]] for i in range(3))


# Find the transformation between two scanners
def match_scanners(scanner_a, scanner_b):
    """Try to match scanner_b to scanner_a by finding overlapping beacons."""
    for rotation in generate_rotations():
        rotated_b = [apply_rotation(beacon, rotation) for beacon in scanner_b]
        offsets = {}
        for a in scanner_dict[scanner_a]:
            for b in rotated_b:
                offset = tuple(a[i] - b[i] for i in range(3))
                offsets[offset] = offsets.get(offset, 0) + 1
                # If 12 beacons overlap, return the transformation
                if offsets[offset] >= 12:
                    translated_b = [tuple(b[i] + offset[i] for i in range(3)) for b in rotated_b]
                    return offset, translated_b
    return None, None


# Solve Part 1 and Part 2
def solve_day19(scanner_dict):
    """Solve Day 19 of Advent of Code."""
    scanners = list(scanner_dict.keys())
    unprocessed = {scanners[0]}
    processed = set()
    all_beacons = set(scanner_dict[scanners[0]])
    scanner_positions = {scanners[0]: (0, 0, 0)}

    while unprocessed:
        current = unprocessed.pop()
        processed.add(current)

        for scanner in scanners:
            if scanner in processed:
                continue
            offset, transformed_beacons = match_scanners(current, scanner_dict[scanner])
            if offset is not None:
                scanner_positions[scanner] = offset
                unprocessed.add(scanner)
                processed.add(scanner)
                all_beacons.update(transformed_beacons)
                scanner_dict[scanner] = transformed_beacons

    # Part 1: Total unique beacons
    part1 = len(all_beacons)

    # Part 2: Maximum Manhattan distance between scanners
    part2 = 0
    scanner_positions = list(scanner_positions.values())
    for i in range(len(scanner_positions)):
        for j in range(i + 1, len(scanner_positions)):
            dist = sum(abs(scanner_positions[i][k] - scanner_positions[j][k]) for k in range(3))
            part2 = max(part2, dist)

    return part1, part2


# Parse input and solve
scanner_dict = parse_scanner_info(input_data)
part1, part2 = solve_day19(scanner_dict)

print(f"Part 1: {part1}")
print(f"Part 2: {part2}")
