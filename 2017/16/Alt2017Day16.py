# Advent of Code - Day 16, Year 2017
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2017/day/16
# Solution by: [abbasmoosajee07]
# Brief: [String Scrambler, P1]

import os, re, copy

# Load the input data from the specified file path
D16_file = "Day16_input.txt"
D16_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D16_file)

with open(D16_file_path) as file:
    input_data = file.read().strip().split(',')

letters_list = [chr(i) for i in range(ord('a'), ord('p') + 1)]

class Scrambler:
    def __init__(self, string):
        self.string = string  # Initialize with the input string

    def display(self):
        # Print the current state of the string
        print(self.string)

    def spin(self, X):
        # Move last X elements to the front
        X = X % len(self.string)  # In case X is larger than the string length
        self.string = self.string[-X:] + self.string[:-X]

    def exchange(self, A, B):
        # Swap positions A and B
        str_list = list(self.string)
        str_list[A], str_list[B] = str_list[B], str_list[A]
        self.string = ''.join(str_list)

    def partner(self, A, B):
        # Swap letters A and B in the string
        A_pos = self.string.find(A)
        B_pos = self.string.find(B)
        
        if A_pos == -1 or B_pos == -1:
            return
        
        self.exchange(A_pos, B_pos)

    def execute(self, command):
        # Execute based on command type
        if command[0] == 'spin':
            self.spin(command[1])
        elif command[0] == 'exchange':
            self.exchange(command[1], command[2])
        elif command[0] == 'partner':
            self.partner(command[1], command[2])


def parse_instruction(instruction):
    # Define regex patterns for spin, exchange, and partner
    spin_pattern = r"s(\d+)"
    exchange_pattern = r"x(\d+)/(\d+)"
    partner_pattern = r"p(\w+)/(\w+)"

    parsed_commands = []

    # Match the command to its appropriate pattern
    spin_match = re.match(spin_pattern, instruction)
    if spin_match:
        X = int(spin_match.group(1))
        parsed_commands.append(('spin', X))
        return parsed_commands

    exchange_match = re.match(exchange_pattern, instruction)
    if exchange_match:
        A, B = map(int, exchange_match.groups())
        parsed_commands.append(('exchange', A, B))
        return parsed_commands

    partner_match = re.match(partner_pattern, instruction)
    if partner_match:
        A, B = partner_match.groups()
        parsed_commands.append(('partner', A, B))
        return parsed_commands

    return parsed_commands


def create_command_list(instruction_list):
    # Parse each instruction into a command list
    command_list = []
    for instruction in instruction_list:
        command = parse_instruction(instruction)
        command_list.extend(command)  # Flatten the parsed commands
    return command_list


def scramble(initial_string, input_data):
    # Initialize Scrambler with the initial string
    scrambler = Scrambler(initial_string)

    # Parse the input data into command list
    command_list = create_command_list(input_data)

    # Execute all commands
    for command in command_list:
        scrambler.execute(command)

    return scrambler.string  # Return the final scrambled result


initial_string = "abcdefghijklmnop"
print(f"Part 1: \n Initial: {initial_string} \n")
print(f"Scrambled: {scramble(initial_string, input_data)} \n")


input_string = initial_string
for iterations in range(0, 1000000000, 1):
    input_string = scramble(input_string, input_data)
    # print(iterations)


print(input_string)