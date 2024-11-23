# Advent of Code - Day 5, Year 2021
# Solution Started: Nov 23, 2024
# Puzzle Link: https://adventofcode.com/2021/day/5
# Solution by: [abbasmoosajee07]
# Brief: [Map Overlapping Wires]
#!/usr/bin/env python3

import os
from collections import defaultdict

# Load the input data
D05_file = "Day05_input.txt"
D05_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D05_file)

with open(D05_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_input(input_data):
    """Parse the input data into a list of line segments."""
    lines = []
    for line in input_data:
        start, end = line.split(" -> ")
        x1, y1 = map(int, start.split(","))
        x2, y2 = map(int, end.split(","))
        lines.append(((x1, y1), (x2, y2)))
    return lines

def get_points_in_line(start, end, include_diagonal=False):
    """Generate all points in a line segment."""
    x1, y1 = start
    x2, y2 = end
    points = []
    
    # Horizontal or vertical lines
    if x1 == x2 or y1 == y2:
        x_range = range(min(x1, x2), max(x1, x2) + 1)
        y_range = range(min(y1, y2), max(y1, y2) + 1)
        points = [(x, y) for x in x_range for y in y_range]
    
    # Diagonal lines (45-degree)
    elif include_diagonal and abs(x1 - x2) == abs(y1 - y2):
        x_step = 1 if x2 > x1 else -1
        y_step = 1 if y2 > y1 else -1
        points = [(x1 + i * x_step, y1 + i * y_step) for i in range(abs(x1 - x2) + 1)]
    
    return points

def count_overlaps(lines, include_diagonal=False):
    """Count points where at least two lines overlap."""
    grid = defaultdict(int)
    
    for start, end in lines:
        points = get_points_in_line(start, end, include_diagonal)
        for point in points:
            grid[point] += 1
    
    # Count points with overlaps
    return sum(1 for count in grid.values() if count > 1)

# Parse the input into a list of line segments
lines = parse_input(input_data)

# Part 1: Count overlaps for horizontal/vertical lines only
part1_result = count_overlaps(lines, include_diagonal=False)
print(f"Part 1: {part1_result}")

# Part 2: Count overlaps including diagonal lines
part2_result = count_overlaps(lines, include_diagonal=True)
print(f"Part 2: {part2_result}")
