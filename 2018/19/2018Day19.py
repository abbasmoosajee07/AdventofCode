# Advent of Code - Day 19, Year 2018
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2018/day/19
# Solution by: [abbasmoosajee07]
# Brief: [Registers Computing]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import collections

# Load the input data from the specified file path
D19_file = "Day19_input.txt"
D19_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D19_file)

# Read and sort input data into a grid
with open(D19_file_path) as file:
    input_data = file.read().strip().split('\n')
    pointer = int(input_data[0][-1])
    instruction_list = input_data[1:]

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

    def _apply_op(self, value):
        result = self.registers.copy()
        result[self.C] = value
        return result

    # Execute a single instruction by calling the correct method
    def execute(self, op, A, B, C):
        self.A, self.B, self.C = A, B, C
        operation = OPERATIONS[op]
        self.registers = operation(self)

# Operations map for easier access
OPERATIONS = {
    'addr': OpcodeComputer.addr,
    'addi': OpcodeComputer.addi,
    'mulr': OpcodeComputer.mulr,
    'muli': OpcodeComputer.muli,
    'banr': OpcodeComputer.banr,
    'bani': OpcodeComputer.bani,
    'borr': OpcodeComputer.borr,
    'bori': OpcodeComputer.bori,
    'setr': OpcodeComputer.setr,
    'seti': OpcodeComputer.seti,
    'gtir': OpcodeComputer.gtir,
    'gtri': OpcodeComputer.gtri,
    'gtrr': OpcodeComputer.gtrr,
    'eqir': OpcodeComputer.eqir,
    'eqri': OpcodeComputer.eqri,
    'eqrr': OpcodeComputer.eqrr,
}

def execute_program(instructions, pointer_register, initial_registers):
    computer = OpcodeComputer(initial_registers)
    ip = 0  # instruction pointer
    
    while 0 <= ip < len(instructions):
        computer.registers[pointer_register] = ip
        instruction, A, B, C = instructions[ip]
        
        # Execute current instruction
        computer.execute(instruction, A, B, C)
        
        # Update instruction pointer from the register it’s bound to
        ip = computer.registers[pointer_register] + 1
        # print(computer.registers)
    return computer.registers

# Parse input data
pointer_register = int(input_data[0][-1])
instructions = []
for line in input_data[1:]:
    parts = line.split()
    op, A, B, C = parts[0], int(parts[1]), int(parts[2]), int(parts[3])
    instructions.append((op, A, B, C))

# Execute the program with initial registers set to 0
initial_registers = [0, 0, 0, 0, 0, 0]
result = execute_program(instructions, pointer_register, initial_registers)
print("Final Registers:", result)
print("Part 1:", result[0])


# Assuming input_data has already been parsed and pointer, instruction_list, etc., are defined
a = int(re.findall(r'\d+', input_data[22])[1])
b = int(re.findall(r'\d+', input_data[24])[1])

# Calculate the number to factorize
number_to_factorize = 10551236 + a * 22 + b

# Function to calculate sum of divisors based on prime factorization
def sum_of_divisors(num):
    factors = collections.defaultdict(lambda: 0)
    possible_prime_divisor = 2
    
    # Factorize the number
    while possible_prime_divisor ** 2 <= num:
        while num % possible_prime_divisor == 0:
            num //= possible_prime_divisor
            factors[possible_prime_divisor] += 1 
        possible_prime_divisor += 1
    if num > 1:
        factors[num] += 1

    # Calculate the sum of divisors from the factors
    sum_div = 1
    for prime_factor in factors:
        sum_div *= (prime_factor ** (factors[prime_factor] + 1) - 1) // (prime_factor - 1)
    return sum_div

# Get the result
result = sum_of_divisors(number_to_factorize)
print("Part 2: Sum of Divisors:", result)
