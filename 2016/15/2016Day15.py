# Advent of Code - Day 15, Year 2016
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2016/day/15
# Solution by: [abbasmoosajee07]
# Brief: [Carousel of Disks]

import os
import re
import math
import numpy as np

# Parse disc information using regex
def get_disc_info(instructions):
    disc_props = []
    for disc in instructions:
        pattern = r'Disc #(\d+) has (\d+) positions; at time=(\d+), it is at position (\d+)\.'
        match = re.search(pattern, disc)
        if match:
            disc_number = int(match.group(1))
            no_pos = int(match.group(2))
            pos_t0 = int(match.group(4))
            disc_props.append(Disc(no_pos, pos_t0))
    return disc_props

# Define Disc class with positions and start_position attributes
class Disc:
    def __init__(self, positions, start_position):
        self.positions = positions
        self.start_position = start_position

    def __repr__(self):
        return f"Disc({self.positions}, {self.start_position})"

# Adjust disc position based on when it's reached
def fixup(i, disc):
    return Disc(disc.positions, (disc.start_position + i) % disc.positions)

# Calculate least common multiple
def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

# Calculate earliest time to pass through a disc
def aux(step_size, wait, disc):
    a, b = disc.positions, disc.start_position
    wait_ = next(i for i in range(wait, wait + step_size * a, step_size) if (i + b) % a == 0)
    return lcm(step_size, a), wait_

# Solve for the earliest time to drop the capsule
def solve(discs):
    step_size, wait = 1, 0
    for i, disc in enumerate(discs, start=1):
        disc = fixup(i, disc)
        step_size, wait = aux(step_size, wait, disc)
    return wait

# Read input from file and return lines
def read_input_file(filename):
    with open(filename) as file:
        return file.read().splitlines()

# Main function to run the solution
def main():
    D15_file = 'Day15_input.txt'
    D15_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D15_file)

    input_lines = read_input_file(D15_file_path)
    discs = get_disc_info(input_lines)

    # Solve part 1
    result1 = solve(discs)
    print(f"Solution for part 1: {result1}")

    # Solve part 2 with an additional disc
    discs_part2 = discs + [Disc(11, 0)]
    result2 = solve(discs_part2)
    print(f"Solution for part 2: {result2}")

# Run the main function
if __name__ == "__main__":
    main()
