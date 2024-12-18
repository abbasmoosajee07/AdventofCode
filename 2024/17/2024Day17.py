"""Advent of Code - Day 17, Year 2024
Solution Started: Dec 17, 2024
Puzzle Link: https://adventofcode.com/2024/day/17
Solution by: abbasmoosajee07
Brief: [Assembly Computer]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D17_file = "Day17_input.txt"
D17_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D17_file)

# Read and sort input data into a grid
with open(D17_file_path) as file:
    input_data = file.read().strip().split('\n\n')

def parse_input(input_info):
    programs = [int(num) for num in input_info[1].strip('Program: ').split(',')]

    register_dict = {}
    for register_input in input_info[0].split('\n'):
        register_strip = register_input.strip('Register ')
        register, value = register_strip.split(': ')
        register_dict[register] = int(value)
    return register_dict, programs

class Chronospatial_Computer:
    def __init__(self, registers, programs):
        self.registers = registers
        self.programs = programs
        self.pointer = 0
        self.output = []

    def dv(self, operand, save_to='A'):  # opcode = 0 (adv), 6 (bdv), 7 (cdv)
        numerator = self.registers['A']
        denominator = 2 ** operand
        divided_num = numerator // denominator
        self.registers[save_to] = divided_num

    def bxl(self, operand):  # opcode = 1
        # Perform XOR operation
        self.registers['B'] = self.registers['B'] ^ operand

    def bst(self, operand):  # opcode = 2
        # Perform combo operand modulo operation
        self.registers['B'] = operand % 8

    def bxc(self, operand):  # opcode = 4
        # Perform XOR operation with register B/C
        self.registers['B'] = self.registers['B'] ^ self.registers['C']

    def out(self, operand):  # opcode = 5
        out_val = operand % 8
        self.output.append(out_val)

    def get_combo_operand(self, operand):
        combo_op = -1
        if 0 <= operand <= 3:
            combo_op = operand
        elif operand == 4:
            combo_op = self.registers['A']
        elif operand == 5:
            combo_op = self.registers['B']
        elif operand == 6:
            combo_op = self.registers['C']
        elif operand == 7:
            pass
        return combo_op

    def process_program(self):
        while self.pointer < len(self.programs):
            opcode = self.programs[self.pointer]
            operand = self.programs[self.pointer + 1]
            combo_op = self.get_combo_operand(operand)

            if opcode == 0:   # adv
                self.dv(combo_op, 'A')
                self.pointer += 2
            elif opcode == 1:  # bxl
                self.bxl(operand)
                self.pointer += 2
            elif opcode == 2:  # bst
                self.bst(combo_op)
                self.pointer += 2
            elif opcode == 3:  # jnz (jump instruction)
                if self.registers['A'] != 0:
                    self.pointer = operand
                else:
                    self.pointer += 2
            elif opcode == 4:  # bxc
                self.bxc(combo_op)
                self.pointer += 2
            elif opcode == 5:  # out
                self.out(combo_op)
                self.pointer += 2
            elif opcode == 6:  # bdv
                self.dv(combo_op, 'B')
                self.pointer += 2
            elif opcode == 7:  # cdv
                self.dv(combo_op, 'C')
                self.pointer += 2

    def get_output(self):
        return ','.join(map(str, self.output))

registers, programs = parse_input(input_data)
processor = Chronospatial_Computer(registers, programs)
processor.process_program()
print("Part 1:", processor.get_output())
