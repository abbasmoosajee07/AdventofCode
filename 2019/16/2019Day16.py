"""Advent of Code - Day 16, Year 2019
Solution Started: Jan 27, 2025
Puzzle Link: https://adventofcode.com/2019/day/16
Solution by: abbasmoosajee07
Brief: [Numbers and Sequences]
"""

#!/usr/bin/env python3

import os, re, copy, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

start_time = time.time()
# Load the input data from the specified file path
D16_file = "Day16_input.txt"
D16_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D16_file)

# Read and sort input data into a grid
with open(D16_file_path) as file:
    input_data = file.read().strip().split()
    input_seq  = list(map(int, input_data[0]))

def analyse_signal(init_sequence: list[int], total_phases: int = 5) -> int:
    def __build_pattern_matrix(seq_len: int):
        """Builds a matrix of patterns for all positions."""
        BASE_PATTERN = [0, 1, 0, -1]
        matrix = {}
        for idx in range(1, seq_len + 1):
            pattern = []
            for num in BASE_PATTERN:
                pattern.extend([num] * idx)  # Repeat each base value `idx` times
            # Skip the first element and trim the pattern to sequence length
            pattern = pattern[1:] + pattern[:1]
            while len(pattern) <= seq_len:
                pattern.extend(pattern)
            pattern_list = pattern[:seq_len]  # Trim the pattern to the sequence length
            matrix[idx] = {pos: pattern_list[pos] for pos in range(seq_len)}
        return matrix

    def __run_phase(start_seq: dict, pattern_matrix: dict) -> dict:
        """Runs one phase of the signal analysis."""
        out_seq = {}
        for pos_1, num_1 in start_seq.items():
            pattern_sel = pattern_matrix[pos_1]
            num_sum = 0
            for pos_2, num_2 in start_seq.items():
                # Use pattern matrix for multiplication
                pattern_num = pattern_sel[pos_2 - 1]
                num_sum += num_2 * pattern_num
            out_seq[pos_1] = abs(num_sum) % 10  # Keep only the last digit
        return out_seq

    # Initialize sequence and pattern matrix
    init_len = len(init_sequence)
    current_sequence = {pos: num for pos, num in enumerate(init_sequence, start=1)}
    pattern_matrix = __build_pattern_matrix(init_len)

    # Process the sequence through all phases
    for phase in range(total_phases):
        current_sequence = __run_phase(current_sequence, pattern_matrix)
        # print(f"Phase {phase + 1}: Start of Sequence: {''.join(map(str, list(current_sequence.values())[:8]))}")

    output_sequence = current_sequence.copy()
    return list(output_sequence.values())

final_output = analyse_signal(input_seq, 100)
print("Part 1:", ''.join(map(str, final_output[:8])))

# print(f"Execution Time = {time.time() - start_time:.5f}s")

