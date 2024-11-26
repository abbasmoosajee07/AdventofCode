# Advent of Code - Day 16, Year 2021
# Solution Started: Nov 25, 2024
# Puzzle Link: https://adventofcode.com/2021/day/16
# Solution by: [abbasmoosajee07]
# Brief: [Binary String Conversion]

#!/usr/bin/env python3

import os, re, copy
from operator import add, mul, gt, lt, eq

# Load the input data from the specified file path
D16_file = "Day16_input.txt"
D16_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D16_file)

# Read and sort input data into a grid
with open(D16_file_path) as file:
    input_data = file.read().strip()


def parse_bits(line):
    # Convert the hex string to bits
    bits = ((int(c, 16) >> i) & 1 for c in line for i in range(3, -1, -1))
    ops = add, mul, lambda *x: min(x), lambda *x: max(x), None, gt, lt, eq
    pos = ver = 0  # Initialize position and version sum

    def read_bits(size):

        nonlocal pos
        pos += size
        return sum(next(bits) << i for i in range(size - 1, -1, -1))

    def parse_packet():
        nonlocal ver
        # Read and add version number
        ver += read_bits(3)

        # Read type ID to decide whether it's a literal value or an operator
        type_id = read_bits(3)

        if type_id == 4:
            # Handle literal value packet
            go, total = read_bits(1), read_bits(4)
            while go:
                go, total = read_bits(1), total << 4 | read_bits(4)
        else:
            # Handle operator packet
            if read_bits(1) == 0:
                # Length-based operator (sub-packets specified by total length)
                length = read_bits(15) + pos
                total = parse_packet()
                while pos < length:
                    total = ops[type_id](total, parse_packet())
            else:
                # Count-based operator (sub-packets specified by number of sub-packets)
                count = read_bits(11)
                total = parse_packet()
                for _ in range(count - 1):
                    total = ops[type_id](total, parse_packet())

        return total

    # Start parsing the root packet and calculate the total
    total_result = parse_packet()

    return ver, total_result

# Parse the data and get the version sum and final result
versions, total = parse_bits(input_data)

# Print the results
print("Part 1:", versions)
print("Part 2:", total)
