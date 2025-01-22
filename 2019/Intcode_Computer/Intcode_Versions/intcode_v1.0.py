# Advent of Code - Day 2, Year 2019
# Solution Started: Nov 17, 2024
# Puzzle Link: https://adventofcode.com/2019/day/2
# Solution by: [abbasmoosajee07]
# Brief: [Intcode CPU v1.0]

#!/usr/bin/env python3

import os, re, copy, sys

class Intcode_CPU:
    def __init__(self, program: list[int], pointer: int = 0, debug: bool = False):
        """
        Initialize the Intcode Program with a copy of the program, a pointer, and optional debugging.
        """
        self.program = program.copy()
        self.pointer = pointer
        self.running = True  # Flag to manage the loop
        self.debug = debug  # Debug flag
        self.opcode_map = {
            1: lambda: self.__arithmetic('add'),
            2: lambda: self.__arithmetic('mult'),
            99: self.__halt,
        }

    def __arithmetic(self, operator: str):
        """
        Perform arithmetic operation based on the operator ('add' or 'mult').
        """
        pointer = self.pointer
        A_addr, B_addr, target = self.program[pointer + 1: pointer + 4]

        if self.debug:
            op_str = f"(A{A_addr}:{self.program[A_addr]}) (B{B_addr}:{self.program[B_addr]}) (to{target}:{self.program[target]})"
            print(f"{pointer:07}: {operator.upper()} {op_str}")

        if operator == 'add':
            self.program[target] = self.program[A_addr] + self.program[B_addr]
        elif operator == 'mult':
            self.program[target] = self.program[A_addr] * self.program[B_addr]

        self.pointer += 4  # Move to the next instruction

    def __halt(self):
        """
        Halt the program and stop execution.
        """
        self.running = False
        if self.debug:
            print(f"{self.pointer:07}: HALT")

    def process_program(self):
        """
        Start and run the Intcode program.
        """
        while self.running:
            opcode = self.program[self.pointer]
            if opcode not in self.opcode_map:
                raise ValueError(f"Unknown opcode {opcode} at position {self.pointer}")

            # Execute the operation based on the opcode
            self.opcode_map[opcode]()  # Executes the correct lambda function or method

        return self.program

def find_address(instruction, target):
    test_instructions = copy.deepcopy(instruction)
    for num_1 in range(10):  # Adjusted range to include 99
        for num_2 in range(10):
            # Create a fresh copy of the instructions for each iteration
            test_instructions = instruction.copy()

            # Set the values at positions 1 and 2
            test_instructions[1] = num_1
            test_instructions[2] = num_2

            # Run the Intcode program
            cpu = Intcode_CPU(test_instructions)
            output_p2 = cpu.process_program()
            print(output_p2[0])
            # Check if the output matches the target
            if output_p2[0] == target:
                return num_1, num_2  # Return the values if found
    return 0, 0

test_program = [1,9,10,3,2,3,11,0,99,30,40,50]

ans_p1 = Intcode_CPU(test_program).process_program()
print("Part 1:", ans_p1[0])

noun, verb = find_address(test_program, 6450)
print("Part 2:", (100 * noun) + verb)

