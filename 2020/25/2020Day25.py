# Advent of Code - Day 25, Year 2020
# Solution Started: Nov 22, 2024
# Puzzle Link: https://adventofcode.com/2020/day/25
# Solution by: [abbasmoosajee07]
# Brief: [Encryption Key]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D25_file = "Day25_input.txt"
D25_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D25_file)

# Read and sort input data into a grid
with open(D25_file_path) as file:
    input_data = file.read().strip().split('\n')

# Constants
M = 20201227

def multiply(x: int, y: int) -> int:
    """Performs modular multiplication."""
    return (x * y) % M

def transform(subject: int, loop: int) -> int:
    """Transforms a subject number based on the loop size."""
    return pow(subject, loop, M)

def decrypt(key: int) -> int:
    """
    Finds the loop size for a given key using the known subject number (7).
    """
    num = 1
    for loop in range(M):
        if num == key:
            return loop
        num = multiply(num, 7)
    raise ValueError("Decryption failed: Loop size not found")

class Solver:
    def __init__(self):
        self.m_a = 0
        self.m_b = 0

    def parse(self, input_data: str):
        """
        Parses the input string to extract integers and assigns them to `m_a` and `m_b`.
        """
        data = list(map(int, input_data))
        self.m_a, self.m_b = data[0], data[1]

    def part1(self):
        """
        Solves part 1 by decrypting the loop size of m_a and transforming m_b with it.
        """
        key = decrypt(self.m_a)
        result = transform(self.m_b, key)
        return result



solver = Solver()
solver.parse(input_data)
ans_p1 = solver.part1()
print("Part 1:", ans_p1)
