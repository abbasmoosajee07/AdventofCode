# Advent of Code - Day 9, Year 2019
# Solution Started: Nov 18, 2024
# Puzzle Link: https://adventofcode.com/2019/day/9
# Solution by: [abbasmoosajee07]
# Brief: [IntCode Computer P5]

#!/usr/bin/env python3

import os

# Load the input data from the specified file path
D09_file = "Day09_input.txt"
D09_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D09_file)

# Read and parse input data into a list of integers
with open(D09_file_path) as file:
    input_data = file.read().strip().split(',')
    input_instructions = [int(num) for num in input_data]

class IntcodeComputer:
    def __init__(self, instructions, inputs=None):
        """Initialize the Intcode computer."""
        self.instructions = instructions[:]  # Copy to avoid modifying the input
        self.memory = {i: v for i, v in enumerate(self.instructions)}  # Dynamic memory
        self.inputs = inputs[:] if inputs else []  # Input queue
        self.outputs = []  # Store outputs
        self.pos = 0  # Instruction pointer
        self.relative_base = 0  # Relative base for mode 2
        self.halted = False  # Whether the program has halted
        self.waiting_for_input = False  # Whether it's waiting for input

    def get_value(self, parameter, mode):
        """Fetch the value based on the parameter mode."""
        if mode == 0:  # Position mode
            return self.memory.get(parameter, 0)
        elif mode == 1:  # Immediate mode
            return parameter
        elif mode == 2:  # Relative mode
            return self.memory.get(self.relative_base + parameter, 0)
        else:
            raise ValueError(f"Unknown parameter mode {mode}")

    def write_value(self, parameter, mode, value):
        """Write a value to memory based on the parameter mode."""
        if mode == 0:  # Position mode
            self.memory[parameter] = value
        elif mode == 2:  # Relative mode
            self.memory[self.relative_base + parameter] = value
        else:
            raise ValueError(f"Invalid mode for writing: {mode}")

    def add_input(self, value):
        """Add a value to the input queue."""
        self.inputs.append(value)
        self.waiting_for_input = False  # Reset waiting state

    def execute(self):
        """Run the Intcode program."""
        while not self.halted:
            # Parse the instruction and modes
            instruction = self.memory.get(self.pos, 0)
            opcode = instruction % 100  # Last two digits
            modes = [(instruction // 10 ** i) % 10 for i in range(2, 5)]  # Parameter modes

            if opcode == 99:  # Halt
                self.halted = True
                break
            
            elif opcode in (1, 2):  # Addition or multiplication
                a = self.get_value(self.memory.get(self.pos + 1, 0), modes[0])
                b = self.get_value(self.memory.get(self.pos + 2, 0), modes[1])
                dest = self.memory.get(self.pos + 3, 0)
                if opcode == 1:  # Add
                    self.write_value(dest, modes[2], a + b)
                elif opcode == 2:  # Multiply
                    self.write_value(dest, modes[2], a * b)
                self.pos += 4
            
            elif opcode == 3:  # Input
                if not self.inputs:
                    self.waiting_for_input = True
                    return None  # Pause execution and wait for input
                dest = self.memory.get(self.pos + 1, 0)
                self.write_value(dest, modes[0], self.inputs.pop(0))
                self.pos += 2
            
            elif opcode == 4:  # Output
                a = self.get_value(self.memory.get(self.pos + 1, 0), modes[0])
                self.outputs.append(a)
                self.pos += 2
                return a  # Produce a single output
            
            elif opcode in (5, 6):  # Jumps
                a = self.get_value(self.memory.get(self.pos + 1, 0), modes[0])
                b = self.get_value(self.memory.get(self.pos + 2, 0), modes[1])
                if (opcode == 5 and a != 0) or (opcode == 6 and a == 0):
                    self.pos = b
                else:
                    self.pos += 3
            
            elif opcode in (7, 8):  # Comparisons
                a = self.get_value(self.memory.get(self.pos + 1, 0), modes[0])
                b = self.get_value(self.memory.get(self.pos + 2, 0), modes[1])
                dest = self.memory.get(self.pos + 3, 0)
                if (opcode == 7 and a < b) or (opcode == 8 and a == b):
                    self.write_value(dest, modes[2], 1)
                else:
                    self.write_value(dest, modes[2], 0)
                self.pos += 4
            
            elif opcode == 9:  # Adjust relative base
                a = self.get_value(self.memory.get(self.pos + 1, 0), modes[0])
                self.relative_base += a
                self.pos += 2
            
            else:
                raise ValueError(f"Unknown opcode {opcode} at position {self.pos}")

        return self.outputs

# Part 1: Execute the Intcode program with input 1
input_p1 = [1]
outputs_p1 = IntcodeComputer(input_instructions, input_p1).execute()
print(f"Part 1: {outputs_p1}")

# Part 2: Execute the Intcode program with input 2
input_p2 = [2]
outputs_p2 = IntcodeComputer(input_instructions, input_p2).execute()
print(f"Part 2: {outputs_p2}")
