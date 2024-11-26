# Advent of Code - Day 22, Year 2021
# Solution Started: Nov 26, 2024
# Puzzle Link: https://adventofcode.com/2021/day/22
# Solution by: [abbasmoosajee07]
# Brief: [Cubes, a lot of Cubes P2]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D22_file = "Day22_input.txt"
D22_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D22_file)

# Read and sort input data into a grid
with open(D22_file_path) as file:
    input_data = file.read().strip()#.split('\n')

import collections
import re

# Named tuples for point and instruction definitions
Point = collections.namedtuple("Point", ["x", "y", "z"])
Instruction = collections.namedtuple("Instruction", ["value", "cuboid"])

class Cuboid:
    def __init__(self, corner1: Point, corner2: Point):
        self.c1 = corner1  # First corner of the cuboid (min corner)
        self.c2 = corner2  # Second corner of the cuboid (max corner)

    def __repr__(self):
        """Return a string representation of the cuboid."""
        return f"Cuboid: {self.c1.x, self.c1.y, self.c1.z}, {self.c2.x, self.c2.y, self.c2.z}"

    def is_valid(self) -> bool:
        """Check if the cuboid is valid (no zero or negative volume)."""
        return (self.c1.x < self.c2.x) and (self.c1.y < self.c2.y) and (self.c1.z < self.c2.z)

    @property
    def volume(self):
        """Calculate and return the volume of the cuboid."""
        return (self.c2.x - self.c1.x) * (self.c2.y - self.c1.y) * (self.c2.z - self.c1.z)

def get_overlap(a: Cuboid, b: Cuboid):
    """Calculate the overlapping cuboid between two cuboids, or return None if no overlap."""
    # Create a potential overlap cuboid by comparing the minimum and maximum coordinates
    overlap = Cuboid(
        Point(max(a.c1.x, b.c1.x), max(a.c1.y, b.c1.y), max(a.c1.z, b.c1.z)),
        Point(min(a.c2.x, b.c2.x), min(a.c2.y, b.c2.y), min(a.c2.z, b.c2.z))
    )
    # If the overlap is valid, return it, else return None
    return overlap if overlap.is_valid() else None

def parse_input(filename: str) -> list[Instruction]:
    """Parse the input file and return a list of instructions."""
    regex = re.compile(r"(on|off) x=(-?[0-9]+)\.\.(-?[0-9]+),y=(-?[0-9]+)\.\.(-?[0-9]+),z=(-?[0-9]+)\.\.(-?[0-9]+)")
    instructions = []
    
    with open(filename, "r") as file:
        for line in file:
            if match := regex.search(line):
                value = match[1] == "on"  # 'on' means True, 'off' means False
                pt1 = Point(int(match[2]), int(match[4]), int(match[6]))
                pt2 = Point(int(match[3]), int(match[5]), int(match[7]))
                
                # Ensure the coordinates are ordered min..max for consistency
                assert pt1 == Point(min(pt1.x, pt2.x), min(pt1.y, pt2.y), min(pt1.z, pt2.z)), \
                    "Input data ordering doesn't comply with expected min..max format"
                assert pt2 == Point(max(pt1.x, pt2.x), max(pt1.y, pt2.y), max(pt1.z, pt2.z)), \
                    "Input data ordering doesn't comply with expected min..max format"
                
                # Adjust to match the correct corner points (add 1 to pt2)
                pt2 = Point(pt2.x + 1, pt2.y + 1, pt2.z + 1)
                cuboid = Cuboid(pt1, pt2)
                instructions.append(Instruction(value, cuboid))
            else:
                assert False, f"Error reading line: {line} -- are the coordinates out of order?"
    
    return instructions

def run_instructions(instructions: list[Instruction]) -> int:
    """Execute all instructions and calculate the total volume of lit cubes."""
    placed = []  # List to keep track of placed cuboids
    total_volume = 0  # Total volume of 'on' cubes

    for instruction in reversed(instructions):
        # If the cuboid is 'on', we calculate its contribution to the total volume
        if instruction.value:
            overlaps = []
            # Check for overlaps with previously placed cuboids
            for cuboid in placed:
                if (overlapping := get_overlap(cuboid, instruction.cuboid)) is not None:
                    # If there's an overlap, we consider it as 'on'
                    overlaps.append(Instruction(True, overlapping))
            # Calculate the volume contributed by the current cuboid
            volume_to_add = instruction.cuboid.volume - run_instructions(overlaps)
            total_volume += volume_to_add

        # Add the current cuboid to the placed list (whether it's on or off)
        placed.append(instruction.cuboid)
    
    # Ensure the total volume is non-negative
    assert total_volume >= 0, "Negative volume shouldn't happen"
    return total_volume

# Load and parse the input file
instructions = parse_input(D22_file_path)

# Calculate the total number of lit cubes and print the result
print(f"Part 2: {run_instructions(instructions)}")
