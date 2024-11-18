# Advent of Code - Day 5, Year 2019
# Solution Started: Nov 17, 2024
# Puzzle Link: https://adventofcode.com/2019/day/5
# Solution by: [abbasmoosajee07]
# Brief: [IntCode Computer P3]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D05_file = "Day05_input.txt"
D05_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D05_file)

# Read and sort input data into a grid
with open(D05_file_path) as file:
    input_data = file.read().strip().split(',')
    input_instructions = [int(num) for num in input_data]

class IntcodeComputer:
    def __init__(self, instructions, inputs):
        self.instructions = instructions[:]  # Copy to avoid modifying the input
        self.inputs = inputs[:]  # Queue for input values
        self.outputs = []  # Store outputs
        self.pos = 0  # Instruction pointer

    def get_value(self, parameter, mode):
        """Fetch the value based on the parameter mode."""
        if mode == 0:  # Position mode
            return self.instructions[parameter]
        elif mode == 1:  # Immediate mode
            return parameter
        else:
            raise ValueError(f"Unknown parameter mode {mode}")

    def execute(self):
        """Run the Intcode program."""
        while True:
            # Parse the instruction and modes
            instruction = self.instructions[self.pos]
            opcode = instruction % 100  # Last two digits
            modes = [(instruction // 10 ** i) % 10 for i in range(2, 5)]  # Parameter modes
            
            if opcode == 99:  # Halt
                break
            
            elif opcode in (1, 2):  # Addition or multiplication
                a = self.get_value(self.instructions[self.pos + 1], modes[0])
                b = self.get_value(self.instructions[self.pos + 2], modes[1])
                dest = self.instructions[self.pos + 3]
                if opcode == 1:  # Add
                    self.instructions[dest] = a + b
                elif opcode == 2:  # Multiply
                    self.instructions[dest] = a * b
                self.pos += 4
            
            elif opcode == 3:  # Input
                if not self.inputs:
                    raise ValueError("Input requested but no inputs available.")
                dest = self.instructions[self.pos + 1]
                self.instructions[dest] = self.inputs.pop(0)
                self.pos += 2
            
            elif opcode == 4:  # Output
                a = self.get_value(self.instructions[self.pos + 1], modes[0])
                self.outputs.append(a)
                self.pos += 2
            
            elif opcode in (5, 6):  # Jumps
                a = self.get_value(self.instructions[self.pos + 1], modes[0])
                b = self.get_value(self.instructions[self.pos + 2], modes[1])
                if (opcode == 5 and a != 0) or (opcode == 6 and a == 0):
                    self.pos = b
                else:
                    self.pos += 3
            
            elif opcode in (7, 8):  # Comparisons
                a = self.get_value(self.instructions[self.pos + 1], modes[0])
                b = self.get_value(self.instructions[self.pos + 2], modes[1])
                dest = self.instructions[self.pos + 3]
                if (opcode == 7 and a < b) or (opcode == 8 and a == b):
                    self.instructions[dest] = 1
                else:
                    self.instructions[dest] = 0
                self.pos += 4
            
            else:
                raise ValueError(f"Unknown opcode {opcode} at position {self.pos}")

        return self.outputs


# Example Usage

input_p1 = [1]
outputs_p1 = IntcodeComputer(input_instructions, input_p1).execute()
ans_p1 = [val for idx, val in enumerate(outputs_p1) if val != 0]
print(f"Part 1: {ans_p1[0]}")


input_p2 = [5]
outputs_p2 = IntcodeComputer(input_instructions, input_p2).execute()
ans_p2 = [val for idx, val in enumerate(outputs_p2) if val != 0]
print(f"Part 2: {ans_p2[0]}")