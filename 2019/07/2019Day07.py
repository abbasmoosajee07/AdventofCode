# Advent of Code - Day 7, Year 2019
# Solution Started: Nov 17, 2024
# Puzzle Link: https://adventofcode.com/2019/day/7
# Solution by: [abbasmoosajee07]
# Brief: [IntCode Computer P4]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import permutations

# Load the input data from the specified file path
D07_file = "Day07_input.txt"
D07_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D07_file)

# Read and sort input data into a grid
with open(D07_file_path) as file:
    input_data = file.read().strip().split(',')
    input_instructions = [int(num) for num in input_data]

class IntcodeComputer:
    def __init__(self, instructions, inputs):
        self.instructions = instructions[:]  # Copy to avoid modifying the input
        self.inputs = inputs[:]  # Queue for input values
        self.outputs = []  # Store outputs
        self.pos = 0  # Instruction pointer
        self.paused = False  # Paused state
        self.halted = False  # Program halt state

    def get_value(self, parameter, mode):
        """Fetch the value based on the parameter mode."""
        if mode == 0:  # Position mode
            return self.instructions[parameter]
        elif mode == 1:  # Immediate mode
            return parameter
        else:
            raise ValueError(f"Unknown parameter mode {mode}")

    def execute(self):
        """Run the Intcode program until halted or paused."""
        while not self.halted:
            instruction = self.instructions[self.pos]
            opcode = instruction % 100
            modes = [(instruction // 10 ** i) % 10 for i in range(2, 5)]
            
            if opcode == 99:  # Halt
                self.halted = True
                break
            
            elif opcode in (1, 2):  # Addition or multiplication
                a = self.get_value(self.instructions[self.pos + 1], modes[0])
                b = self.get_value(self.instructions[self.pos + 2], modes[1])
                dest = self.instructions[self.pos + 3]
                self.instructions[dest] = a + b if opcode == 1 else a * b
                self.pos += 4
            
            elif opcode == 3:  # Input
                if not self.inputs:
                    self.paused = True
                    return None  # Wait for more input
                dest = self.instructions[self.pos + 1]
                self.instructions[dest] = self.inputs.pop(0)
                self.pos += 2
            
            elif opcode == 4:  # Output
                a = self.get_value(self.instructions[self.pos + 1], modes[0])
                self.outputs.append(a)
                self.pos += 2
                self.paused = True
                return a  # Return output immediately
            
            elif opcode in (5, 6):  # Jumps
                a = self.get_value(self.instructions[self.pos + 1], modes[0])
                b = self.get_value(self.instructions[self.pos + 2], modes[1])
                self.pos = b if (opcode == 5 and a != 0) or (opcode == 6 and a == 0) else self.pos + 3
            
            elif opcode in (7, 8):  # Comparisons
                a = self.get_value(self.instructions[self.pos + 1], modes[0])
                b = self.get_value(self.instructions[self.pos + 2], modes[1])
                dest = self.instructions[self.pos + 3]
                self.instructions[dest] = int((opcode == 7 and a < b) or (opcode == 8 and a == b))
                self.pos += 4
            
            else:
                raise ValueError(f"Unknown opcode {opcode} at position {self.pos}")
        return None



def run_amplifiers(program, phase_settings):
    max_signal = 0
    for phases in permutations(phase_settings):
        amplifiers = [IntcodeComputer(program, [phase]) for phase in phases]
        signal = 0
        halted = False
        while not halted:
            for amp in amplifiers:
                amp.inputs.append(signal)
                output = amp.execute()
                if output is not None:
                    signal = output
                halted = all(a.halted for a in amplifiers)
        max_signal = max(max_signal, signal)
    return max_signal

ans_p1 = run_amplifiers(input_instructions, range(0, 5))
print(f"Part 1: {ans_p1}")  # Part 1
ans_p2 = run_amplifiers(input_instructions, range(5, 10))
print(f"Part 2: {ans_p2}") 
