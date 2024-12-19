"""Advent of Code - Day 17, Year 2024
Solution Started: Dec 17, 2024
Puzzle Link: https://adventofcode.com/2024/day/17
Solution by: abbasmoosajee07
Brief: [Assembly Computer]
"""

#!/usr/bin/env python3

import os, re, copy, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

start_time = time.time()

# Load the input data from the specified file path
D17_file = "Day17_input.txt"
D17_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D17_file)

with open(D17_file_path) as file:
    input_data = file.read().strip().split('\n\n')

class State:
    def __init__(self, registers: dict):
        self.registers = registers
        self.pointer = 0
        self.output = []

    def __getitem__(self, index):
        return self.registers[index]

    def __setitem__(self, index, value: int):
        self.registers[index] = value

    def increment_pointer(self):
        self.pointer += 1

    def reset(self, a):
        self.registers = {'A': a, 'B': 0, 'C': 0}
        self.output = []
        self.pointer = 0

    def oct_to_dec(octal_str: str) -> int:
        return int(octal_str, 8)

    def dec_to_oct(decimal: int) -> str:
        return format(decimal, 'o')

class Chronospatial_Computer():
    def __init__(self, operand: int):
        self.operand = operand

    def combo_operand(self, registers: State):
        operand_mapping = {4: 'A', 5: 'B', 6: 'C'}
        if self.operand in operand_mapping:
            return registers[operand_mapping[self.operand]]
        return self.operand

    def adv(self, registers: State):
        denominator = self.combo_operand(registers)
        registers['A'] //= 2 ** denominator
        registers.increment_pointer()

    def bxl(self, registers: State):
        registers['B'] ^= self.operand
        registers.increment_pointer()

    def bst(self, registers: State):
        registers['B'] = self.combo_operand(registers) % 8
        registers.increment_pointer()

    def jnz(self, registers: State):
        if registers['A'] != 0:
            registers.pointer = self.operand
        else:
            registers.increment_pointer()

    def bxc(self, registers: State):
        registers['B'] ^= registers['C']
        registers.increment_pointer()

    def out(self, registers: State):
        registers.output.append(self.combo_operand(registers) % 8)
        registers.increment_pointer()

    def bdv(self, registers: State):
        registers['B'] = registers['A'] // (2 ** self.combo_operand(registers))
        registers.increment_pointer()

    def cdv(self, registers: State):
        registers['C'] = registers['A'] // (2 ** self.combo_operand(registers))
        registers.increment_pointer()

def parse_input(input_info: list) -> tuple[State, list[tuple]]:
    registers = State({'A': 0, 'B': 0, 'C': 0})
    instructions = []

    for line in input_info[0].split('\n'):
        register_value = int(line.rsplit(maxsplit=1)[-1])
        if 'A' in line:
            registers['A'] = register_value
        elif 'B' in line:
            registers['B'] = register_value
        elif 'C' in line:
            registers['C'] = register_value

    program = input_info[1].split(maxsplit=1)[-1].split(',')
    for i in range(0, len(program), 2):
        opcode = int(program[i])
        operand = int(program[i + 1])
        instructions.append((opcode, operand))  # Store the opcode and operand

    return registers, instructions

def run_computer(registers: dict, instructions: list) -> str:

    while registers.pointer < len(instructions):
        opcode, operand = instructions[registers.pointer]
        processor = Chronospatial_Computer(operand)  # Create a Processor instance
        instruction_method = getattr(processor, ['adv', 'bxl', 'bst', 'jnz', 'bxc', 'out', 'bdv', 'cdv'][opcode])
        instruction_method(registers)

    return ','.join(map(str, registers.output))  # Return the output after processing all instructions

def disassemble_code(registers: dict, instructions: list) -> int:
    output_sequence = [item for instr in instructions for item in (instr[0], instr[1])]  # Adjusted to use the tuple

    lower_bound = 0
    for i in range(len(output_sequence) - 1, -1, -1):
        for a in range(lower_bound, lower_bound + (8 ** (len(output_sequence) - i))):
            registers.reset(a)
            while registers.pointer < len(instructions):
                opcode, operand = instructions[registers.pointer]
                processor = Chronospatial_Computer(operand)  # Create a Processor instance
                instruction_method = getattr(processor, ['adv', 'bxl', 'bst', 'jnz', 'bxc', 'out', 'bdv', 'cdv'][opcode])
                instruction_method(registers)  # Execute the instruction

            if registers.output == output_sequence[i:]:
                if len(registers.output) == len(output_sequence):
                    return a

                lower_bound = State.oct_to_dec(State.dec_to_oct(a) + '0')
                break

registers, instructions = parse_input(input_data)

print("Part 1:", run_computer(registers, instructions))

print("Part 2:", disassemble_code(registers, instructions))

print(time.time() - start_time)
