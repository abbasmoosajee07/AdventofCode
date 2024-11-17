# Advent of Code - Day 2, Year 2019
# Solution Started: Nov 17, 2024
# Puzzle Link: https://adventofcode.com/2019/day/2  # Web link without padding
# Solution by: [abbasmoosajee07]
# Brief: [IntCode Computer P1]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D02_file = "Day02_input.txt"
D02_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D02_file)

# Read and sort input data into a grid
with open(D02_file_path) as file:
    input_data = file.read().strip().split(',')
    input_list = [int(num) for num in input_data]
og_instructions = copy.deepcopy(input_list)

class IntcodeComputer:
    def __init__(self, instructions):
        self.instructions = instructions[:]  # Make a copy to avoid modifying the input
        self.pos = 0

    def int_add(self):
        """Perform addition as per Opcode 1."""
        a, b, dest = self.instructions[self.pos + 1:self.pos + 4]
        self.instructions[dest] = self.instructions[a] + self.instructions[b]

    def int_mult(self):
        """Perform multiplication as per Opcode 2."""
        a, b, dest = self.instructions[self.pos + 1:self.pos + 4]
        self.instructions[dest] = self.instructions[a] * self.instructions[b]

    def get_current_opcode(self):
        """Get the current opcode."""
        return self.instructions[self.pos]

    def advance(self):
        """Move the instruction pointer to the next block."""
        self.pos += 4

    def is_halted(self):
        """Check if the program is halted."""
        return self.instructions[self.pos] == 99


def execute(computer):
    """Execute the Intcode program using the IntcodeComputer."""
    while not computer.is_halted():  # Run until Opcode 99 is encountered
        opcode = computer.get_current_opcode()
        if opcode == 1:  # Addition
            computer.int_add()
        elif opcode == 2:  # Multiplication
            computer.int_mult()
        else:
            raise ValueError(f"Unknown opcode {opcode} at position {computer.pos}")
        computer.advance()  # Move to the next instruction block
    return computer.instructions  # Return the final state of the program

instruction_p1 = input_list
instruction_p1[1] = 12
instruction_p1[2] = 2

computer = IntcodeComputer(instruction_p1)

ans_p1 = execute(computer)
print(f"Part 1: {ans_p1[0]}")


def find_address(instruction, target):
    for num_1 in range(99):
        for num_2 in range(99):
            instruction[1] = num_1
            instruction[2] = num_2

            computer = IntcodeComputer(instruction)

            output_p2 = execute(computer)
            if output_p2[0] == target:
                address = (100 * num_1) + num_2
                break
    return address

ans_p2 = find_address(input_list, 19690720)
print(f"Part 2: {ans_p2}")
