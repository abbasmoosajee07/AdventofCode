# Advent of Code - Day 13, Year 2019
# Solution Started: Jan 24, 2025
# Puzzle Link: https://adventofcode.com/2019/day/13
# Solution by: [abbasmoosajee07]
# Brief: [IntCode Arcade Game]

#!/usr/bin/env python3

import os, sys

intcode_path = os.path.join(os.path.dirname(__file__), "..", "Intcode_Computer")
sys.path.append(intcode_path)

from Intcode_Computer import Intcode_CPU

# Load the input data from the specified file path
D13_file = "Day13_input.txt"
D13_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D13_file)



# Read and parse input data
with open(D13_file_path) as file:
    input_data = file.read().strip().split(',')
    input_program = [int(num) for num in input_data]

def start_game(game_software):
    robot_cpu = Intcode_CPU(game_software)
    robot_cpu.process_program()
    output = robot_cpu.get_result('output')
    tile_list = list(zip(output[::3], output[1::3], output[2::3]))
    return tile_list

exit_tiles = start_game(input_program)
block_count = sum(1 for _, _, tile in exit_tiles if tile == 2)

print("Part 1:", block_count)
