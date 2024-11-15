# Advent of Code - Day 8, Year 2016
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2016/day/8
# Solution by: [abbasmoosajee07]
# Brief: [2FA and rolling codes]

import os
import re
import numpy as np

# Define the input file path
D8_file = 'Day08_input.txt'
D8_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D8_file)

# Read input file
with open(D8_file_path) as file:
    input_lines = file.read().splitlines()
    

class Screen:
    def __init__(self, width, height):
        # Initialize screen with all pixels off (0)
        self.screen = np.zeros((height, width), dtype=int)

    def display(self):
        # Print the screen, with 1s as "#" and 0s as "."
        for row in self.screen:
            print("".join("#" if pixel else "." for pixel in row))
        print()

    def rect(self, A, B):
        # Turn on all pixels in a rectangle at the top-left corner of width A and height B
        self.screen[:B, :A] = 1

    def rotate_row(self, A, B):
        # Shift row A right by B pixels, and allow roll over
        self.screen[A] = np.roll(self.screen[A], B)

    def rotate_column(self, A, B):
        # Shift column A down by B pixels, and allow roll over
        self.screen[:, A] = np.roll(self.screen[:, A], B)

    def execute(self, command):
        # Execute the parsed command
        if command[0] == 'rect':
            self.rect(command[1], command[2])
        elif command[0] == 'rotate_row':
            self.rotate_row(command[1], command[2])
        elif command[0] == 'rotate_column':
            self.rotate_column(command[1], command[2])
            
    def sum_screen(self):
        # Sum all the 'on' pixels (1s)
        return np.sum(self.screen)


def parse_instruction(instruction):
    # List to store parsed commands
    parsed_commands = []

    # Regular expressions for each command
    rect_pattern = r"rect (\d+)x(\d+)"
    rotate_row_pattern = r"rotate row y=(\d+) by (\d+)"
    rotate_column_pattern = r"rotate column x=(\d+) by (\d+)"

    # Split the instruction by newlines
    commands = instruction.split('\n')

    for command in commands:
        # Match the 'rect' command
        rect_match = re.match(rect_pattern, command)
        if rect_match:
            A, B = map(int, rect_match.groups())
            parsed_commands.append(('rect', A, B))
            continue

        # Match the 'rotate row' command
        row_match = re.match(rotate_row_pattern, command)
        if row_match:
            row, shift = map(int, row_match.groups())
            parsed_commands.append(('rotate_row', row, shift))
            continue

        # Match the 'rotate column' command
        column_match = re.match(rotate_column_pattern, command)
        if column_match:
            col, shift = map(int, column_match.groups())
            parsed_commands.append(('rotate_column', col, shift))
            continue

    return parsed_commands


# Example usage:
width, height =  50, 6 # Create a screen of width 7 and height 3
screen = Screen(width, height)

# Loop through the instructions and execute them
for instruction in input_lines:
    # Parse and execute each instruction
    commands = parse_instruction(instruction)
    for command in commands:
        screen.execute(command)

    # Optionally, display the screen after each instruction


# Sum the total number of 'on' pixels
total_on_pixels = screen.sum_screen()
print(f"Total 'on' pixels: {total_on_pixels}")

screen.display()