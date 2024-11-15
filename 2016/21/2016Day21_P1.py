# Advent of Code - Day 21, Year 2016
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2016/day/21
# Solution by: [abbasmoosajee07]
# Brief: [String Scrambler, P1]

import os
import re
import numpy as np

# Example file name (adjust the path as needed)
D21_file = 'Day21_input.txt'
D21_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D21_file)

# Load the input
with open(D21_file_path) as file:
    input_data = file.read().splitlines()

class Scrambler:
    def __init__(self, string):
        self.string = string  # Initialize with the input string

    def display(self):
        # Print the current state of the string
        print(self.string)

    def swap_letter(self, A, B):
        A_pos = self.string.find(A)
        B_pos = self.string.find(B)
        
        if A_pos == -1 or B_pos == -1:
            return
        
        str_list = list(self.string)
        str_list[A_pos], str_list[B_pos] = str_list[B_pos], str_list[A_pos]
        self.string = ''.join(str_list)

    def swap_position(self, A_pos, B_pos):
        str_list = list(self.string)
        str_list[A_pos], str_list[B_pos] = str_list[B_pos], str_list[A_pos]
        self.string = ''.join(str_list)

    def rotate_steps(self, steps, sign):
        steps = steps % len(self.string)  # Handle steps greater than string length
        if sign > 0:
            self.string = self.string[-steps:] + self.string[:-steps]
        else:
            self.string = self.string[steps:] + self.string[:steps]

    def rotate_letter(self, letter):
        idx = self.string.find(letter)
        if idx == -1:
            return
        
        steps = 1 + idx + (1 if idx >= 4 else 0)
        self.rotate_steps(steps, 1)

    def reverse_positions(self, x, y):
        if x < 0 or y >= len(self.string) or x > y:
            return
        
        self.string = self.string[:x] + self.string[x:y + 1][::-1] + self.string[y + 1:]

    def move_position(self, x, y):
        if x < 0 or x >= len(self.string) or y < 0 or y >= len(self.string):
            return
        
        char = self.string[x]
        self.string = self.string[:x] + self.string[x + 1:]
        self.string = self.string[:y] + char + self.string[y:]

    def execute(self, command):
        if command[0] == 'swap_position':
            self.swap_position(command[1], command[2])
        elif command[0] == 'swap_letter':
            self.swap_letter(command[1], command[2])
        elif command[0] == 'reverse_positions':
            self.reverse_positions(command[1], command[2])
        elif command[0] == 'rotate_steps':
            self.rotate_steps(command[3], command[2])
        elif command[0] == 'move_position':
            self.move_position(command[1], command[2])
        elif command[0] == 'rotate_letter':
            self.rotate_letter(command[1])

def parse_instruction(instruction):
    parsed_commands = []
    swap_pos_pattern = r"swap position (\d+) with position (\d+)"
    swap_letter_pattern = r"swap letter (\w+) with letter (\w+)"
    rotate_steps_pattern = r"rotate (left|right) (\d+) steps?"
    rotate_pos_pattern = r"rotate based on position of letter (\w+)"
    reverse_pos_pattern = r"reverse positions (\d+) through (\d+)"
    move_pos_pattern = r"move position (\d+) to position (\d+)"

    commands = instruction.split('\n')

    for command in commands:
        swap_pos_match = re.match(swap_pos_pattern, command)
        if swap_pos_match:
            X, Y = map(int, swap_pos_match.groups())
            parsed_commands.append(('swap_position', X, Y))
            continue

        swap_letter_match = re.match(swap_letter_pattern, command)
        if swap_letter_match:
            X, Y = swap_letter_match.groups()
            parsed_commands.append(('swap_letter', X, Y))
            continue
        
        rotate_steps_match = re.match(rotate_steps_pattern, command)
        if rotate_steps_match:
            direction, steps = rotate_steps_match.groups()
            steps = int(steps)
            sign = 1 if direction == "right" else -1
            parsed_commands.append(('rotate_steps', direction, sign, steps))
            continue

        rotate_pos_match = re.match(rotate_pos_pattern, command)
        if rotate_pos_match:
            letter = rotate_pos_match.group(1)
            parsed_commands.append(('rotate_letter', letter))
            continue

        reverse_pos_match = re.match(reverse_pos_pattern, command)
        if reverse_pos_match:
            X, Y = map(int, reverse_pos_match.groups())
            parsed_commands.append(('reverse_positions', X, Y))
            continue

        move_pos_match = re.match(move_pos_pattern, command)
        if move_pos_match:
            X, Y = map(int, move_pos_match.groups())
            parsed_commands.append(('move_position', X, Y))
            continue

    return parsed_commands

def create_command_list(instruction_list):
    command_list = []
    for instruction in instruction_list:
        command = parse_instruction(instruction)
        command_list.append(command)
    return command_list

def scramble(initial_string, input_data):
    scrambler = Scrambler(initial_string)

    command_list = create_command_list(input_data)

    # Execute all commands
    for commands in command_list:
        for command in commands:
            scrambler.execute(command)

    return scrambler.string  # Return the final scrambled result


initial_string = "abcdefgh"
print(f"Part 1: \n Initial: {initial_string} \n")
print(f" Scrambled: {scramble(initial_string, input_data)} \n")


