# Advent of Code - Day 21, Year 2018
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2018/day/21
# Solution by: [abbasmoosajee07]
# Brief: [Computing Registers, Really LONNG]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

# Start the timer
start_time = time.time()

# Load the input data from the specified file path
D21_file = "Day21_input.txt"
D21_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D21_file)

# Read and sort input data into a grid
with open(D21_file_path) as file:
    input_data = file.read().strip().split('\n')

# Get instruction pointer and instructions
pointer_register = int(input_data[0][-1])
instructions = [
    (line.split()[0], int(line.split()[1]), int(line.split()[2]), int(line.split()[3]))
    for line in input_data[1:]
]

class OpcodeComputer:
    def __init__(self, registers):
        self.registers = registers

    # Add Registers
    def addr(self): return self._apply_op(self.registers[self.A] + self.registers[self.B])
    def addi(self): return self._apply_op(self.registers[self.A] + self.B)

    # Multiply Registers
    def mulr(self): return self._apply_op(self.registers[self.A] * self.registers[self.B])
    def muli(self): return self._apply_op(self.registers[self.A] * self.B)

    # Bitwise AND
    def banr(self): return self._apply_op(self.registers[self.A] & self.registers[self.B])
    def bani(self): return self._apply_op(self.registers[self.A] & self.B)

    # Bitwise OR
    def borr(self): return self._apply_op(self.registers[self.A] | self.registers[self.B])
    def bori(self): return self._apply_op(self.registers[self.A] | self.B)

    # Assignment operations
    def setr(self): return self._apply_op(self.registers[self.A])
    def seti(self): return self._apply_op(self.A)

    # Greater-than testing
    def gtir(self): return self._apply_op(1 if self.A > self.registers[self.B] else 0)
    def gtri(self): return self._apply_op(1 if self.registers[self.A] > self.B else 0)
    def gtrr(self): return self._apply_op(1 if self.registers[self.A] > self.registers[self.B] else 0)

    # Equality testing
    def eqir(self): return self._apply_op(1 if self.A == self.registers[self.B] else 0)
    def eqri(self): return self._apply_op(1 if self.registers[self.A] == self.B else 0)
    def eqrr(self): return self._apply_op(1 if self.registers[self.A] == self.registers[self.B] else 0)

    # Apply the operation to the registers
    def _apply_op(self, value):
        result = self.registers.copy()
        result[self.C] = value
        self.registers = result

    # Execute a single instruction
    def execute(self, op, A, B, C):
        self.A, self.B, self.C = A, B, C
        operation = OPERATIONS[op]
        operation(self)

# Operations map
OPERATIONS = {
    'addr': OpcodeComputer.addr, 'addi': OpcodeComputer.addi,
    'mulr': OpcodeComputer.mulr, 'muli': OpcodeComputer.muli,
    'banr': OpcodeComputer.banr, 'bani': OpcodeComputer.bani,
    'borr': OpcodeComputer.borr, 'bori': OpcodeComputer.bori,
    'setr': OpcodeComputer.setr, 'seti': OpcodeComputer.seti,
    'gtir': OpcodeComputer.gtir, 'gtri': OpcodeComputer.gtri,
    'gtrr': OpcodeComputer.gtrr,
    'eqir': OpcodeComputer.eqir, 'eqri': OpcodeComputer.eqri,
    'eqrr': OpcodeComputer.eqrr,
}

def execute_program(instructions, pointer_register, initial_registers):
    computer = OpcodeComputer(initial_registers)
    seen_values = set()
    last_value = None
    ip = 0  # instruction pointer

    while 0 <= ip < len(instructions):
        computer.registers[pointer_register] = ip
        instruction, A, B, C = instructions[ip]

        # Execute the current instruction
        computer.execute(instruction, A, B, C)

        # Part 1 & Part 2 special check for the eqrr instruction
        if instruction == 'eqrr':
            current_value = computer.registers[A]  # Observing the specific register
            if current_value not in seen_values:
                seen_values.add(current_value)
                if last_value is None:
                    print("Part 1:", current_value)  # First halt condition for Part 1
                    last_value = current_value
                    break
            else:
                print("Part 2:", last_value)  # Last unique value before repeat for Part 2
                break

        # Update the instruction pointer
        ip = computer.registers[pointer_register] + 1

# Execute the program with initial registers set to 0
initial_registers = [0] * 6
execute_program(instructions, pointer_register, initial_registers)

# Stop the timer
end_time = time.time()

# Calculate elapsed time
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")