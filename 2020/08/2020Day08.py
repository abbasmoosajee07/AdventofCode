# Advent of Code - Day 8ear 2020
# Solution Started: Nov 20, 2024
# Puzzle Link: https://adventofcode.com/2020/day/8
# Solution by: [abbasmoosajee07]
# Brief: [Assembly Computer]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D08_file = "Day08_input.txt"
D08_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D08_file)

# Read and sort input data into a grid
with open(D08_file_path) as file:
    input_data = file.read().strip()

import pandas as pd

class AssemblyComputer:
    def __init__(self):
        self.acc = 0       # Accumulator starts at 0
        self.pointer = 0   # Instruction pointer (position)

    def acc_command(self, operand):
        """Increase or decrease the accumulator."""
        self.acc += int(operand)
        self.pointer += 1  # Move to the next instruction

    def jmp_command(self, operand):
        """Jump to a new instruction based on the offset."""
        self.pointer += int(operand)

    def nop_command(self):
        """No operation, move to the next instruction."""
        self.pointer += 1

    def execute_command(self, command, operand):
        """Execute the specified command."""
        if command == 'acc':
            self.acc_command(operand)
        elif command == 'jmp':
            self.jmp_command(operand)
        elif command == 'nop':
            self.nop_command()
        else:
            raise ValueError(f"Unknown command: {command}")

    def run(self, instructions):
        """
        Run the program until an instruction is about to repeat or the program terminates.
        Returns:
        - acc: Accumulator value before the program halts or repeats.
        - terminated: Whether the program terminated successfully (True) or encountered an infinite loop (False).
        """
        executed_instructions = set()

        while self.pointer not in executed_instructions and 0 <= self.pointer < len(instructions):
            executed_instructions.add(self.pointer)

            command, operand = instructions[self.pointer]
            self.execute_command(command, operand)

        terminated = self.pointer >= len(instructions)
        return self.acc, terminated

# Helper function to parse input into a list of instructions
def parse_instructions(input_data):
    """
    Parse the input data into a list of instructions.
    Each line is split into a command and its operand.
    """
    instructions = []
    for line in input_data.strip().split('\n'):
        command, operand = line.split()
        instructions.append((command, operand))
    return instructions

# Part 1: Detect the infinite loop
def solve_part_1(input_data):
    """Find the accumulator value before the infinite loop occurs."""
    instructions = parse_instructions(input_data)
    computer = AssemblyComputer()
    acc_value, _ = computer.run(instructions)
    return acc_value

# Part 2: Fix the program
def solve_part_2(input_data):
    """Fix the program and return the accumulator value after it terminates."""
    instructions = parse_instructions(input_data)

    for i in range(len(instructions)):
        # Only consider 'nop' and 'jmp' instructions for modification
        command, operand = instructions[i]
        if command not in ('nop', 'jmp'):
            continue

        # Modify the instruction
        modified_instructions = instructions.copy()
        modified_instructions[i] = ('jmp' if command == 'nop' else 'nop', operand)

        # Test the modified program
        computer = AssemblyComputer()
        acc_value, terminated = computer.run(modified_instructions)

        if terminated:
            return acc_value

    return None



# Solve Part 1
part_1_result = solve_part_1(input_data)
print(f"Part 1: {part_1_result}")

# Solve Part 2
part_2_result = solve_part_2(input_data)
print(f"Part 2: {part_2_result}")
