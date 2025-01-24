# Advent of Code - Day 7, Year 2019
# Solution Started: Jan 22, 2025
# Puzzle Link: https://adventofcode.com/2019/day/7
# Solution by: [abbasmoosajee07]
# Brief: [IntCode Computer v3]

#!/usr/bin/env python3

import os, re, copy, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import permutations

intcode_path = os.path.join(os.path.dirname(__file__), "..", "Intcode_Computer")
sys.path.append(intcode_path)

from Intcode_Computer import Intcode_CPU
# Load the input data from the specified file path
D07_file = "Day07_input.txt"
D07_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D07_file)

# Read and sort input data into a grid
with open(D07_file_path) as file:
    input_data = file.read().strip().split(',')
    input_program = [int(num) for num in input_data]

def run_amplifiers(program, phase_settings):
    max_signal = 0
    for phases in permutations(phase_settings):
        amplifiers = [Intcode_CPU(program, init_inputs=[phase], debug=False, add_input=True) for phase in phases]
        signal = 0

        while any(a.running for a in amplifiers):  # Run until all amplifiers halt
            for amp in amplifiers:
                if amp.paused:
                    amp.paused = False  # Resume if paused
                amp.process_program(external_input=signal)
                if amp.output_list:  # Check if there's a new output
                    signal = amp.output_list.pop(0)

        max_signal = max(max_signal, signal)

    return max_signal


ans_p1 = run_amplifiers(input_program, range(0, 5))
print(f"Part 1: {ans_p1}")

ans_p2= run_amplifiers(input_program, range(5, 10))
print(f"Part 2: {ans_p2}")