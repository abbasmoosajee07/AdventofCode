# Advent of Code - Day 18, Year 2017
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2017/day/18
# Solution by: [abbasmoosajee07]
# Brief: [Computing Registers]

import os, re, copy
import pandas as pd
import numpy as np
# Load the input data from the specified file path
D18_file = "Day18_input.txt"
D18_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D18_file)

with open(D18_file_path) as file:
    input_data = file.read().strip().split('\n')

# Parse the input data into a DataFrame
def parse_instructions(input_data):
    commands = []
    for line in input_data:
        parts = line.split()
        # Ensure we handle missing 'Y' by filling it with None
        command = parts[0]
        X = parts[1] if len(parts) > 1 else None
        Y = parts[2] if len(parts) > 2 else None
        commands.append((command, X, Y))
    return pd.DataFrame(commands, columns=['command', 'X', 'Y'])

class SoundProcessor:
    def __init__(self):
        self.registers = {}
        self.last_sound = None
        self.pointer = 0

    def get_value(self, operand):
        """Return the integer value of operand or register content if it's a register."""
        if operand is None:
            return 0
        if isinstance(operand, int) or operand.lstrip('-').isdigit():
            return int(operand)
        return self.registers.get(operand, 0)

    def snd(self, X):
        """Play sound with the frequency given by the value of X."""
        self.last_sound = self.get_value(X)

    def set_reg(self, X, Y):
        """Set register X to the value of Y."""
        self.registers[X] = self.get_value(Y)

    def add(self, X, Y):
        """Increase register X by the value of Y."""
        self.registers[X] = self.registers.get(X, 0) + self.get_value(Y)

    def mul(self, X, Y):
        """Set register X to the result of multiplying register X by Y."""
        self.registers[X] = self.registers.get(X, 0) * self.get_value(Y)

    def mod(self, X, Y):
        """Set register X to the remainder of dividing register X by Y."""
        if self.get_value(Y) != 0:
            self.registers[X] = self.registers.get(X, 0) % self.get_value(Y)

    def rcv(self, X):
        """Recover the frequency of the last sound if X is non-zero."""
        if self.get_value(X) != 0:
            print(f"Recovered frequency: {self.last_sound}")
            return self.last_sound
        return None

    def jgz(self, X, Y):
        """Jump with an offset of Y if X is greater than zero."""
        if self.get_value(X) > 0:
            return self.get_value(Y)
        return 1

    def execute_command(self, command, X, Y):
        if command == 'snd':
            self.snd(X)
        elif command == 'set':
            self.set_reg(X, Y)
        elif command == 'add':
            self.add(X, Y)
        elif command == 'mul':
            self.mul(X, Y)
        elif command == 'mod':
            self.mod(X, Y)
        elif command == 'rcv':
            result = self.rcv(X)
            if result is not None:
                return result
        elif command == 'jgz':
            offset = self.jgz(X, Y)
            self.pointer += offset - 1  # Adjust pointer by offset-1 to account for pointer increment in `run`
        return None

    def run(self, df):
        """Execute instructions until an `rcv` command recovers a frequency or instructions end."""
        while 0 <= self.pointer < len(df):
            command, X, Y = df.iloc[self.pointer]
            result = self.execute_command(command, X, Y)
            if result is not None:
                return result
            self.pointer += 1

# Example usage
df = parse_instructions(input_data)
processor = SoundProcessor()
recovered_frequency = processor.run(df)
print(f"The first recovered frequency is: {recovered_frequency}")
