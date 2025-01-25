# Advent of Code - Day 7, Year 2019
# Solution Started: Jan 22, 2025
# Puzzle Link: https://adventofcode.com/2019/day/7
# Solution by: [abbasmoosajee07]
# Brief: [IntCode Computer v3]

#!/usr/bin/env python3

import os, re, copy, sys

intcode_path = os.path.join(os.path.dirname(__file__), "..", "Intcode_Computer")
sys.path.append(intcode_path)

# Load the input data from the specified file path
D07_file = "Day07_input.txt"
D07_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D07_file)

# Read and sort input data into a grid
with open(D07_file_path) as file:
    input_data = file.read().strip().split(',')
    input_program = [int(num) for num in input_data]

class Intcode_Amplifiers:
    """
    Class to simulate a set of Intcode amplifiers with a feedback loop,
    running different phase settings to find the maximum output signal.
    """
    def __init__(self, program):
        from itertools import permutations
        from Intcode_Computer import Intcode_CPU
        self.Intcode_CPU = Intcode_CPU  # Reference to Intcode_CPU for amplifier execution
        self.program = program  # The Intcode program to be executed
        self.permutations = permutations  # Helper function to generate phase setting permutations

    def run_amplifiers(self, phase_settings):
        """
        Runs amplifiers with different phase settings and returns the maximum signal produced.
        """
        max_signal = 0  # Initialize the maximum signal
        for phases in self.permutations(phase_settings):  # Iterate through phase permutations
            amplifiers = [self.Intcode_CPU(self.program, init_inputs=[phase], debug=False) for phase in phases]
            signal = 0  # Initial signal for the first amplifier

            # Run until all amplifiers halt
            while any(a.running for a in amplifiers):
                for amp in amplifiers:
                    if amp.paused:
                        amp.paused = False  # Resume paused amplifiers
                    amp.process_program(external_input=signal)  # Run the amplifier
                    if amp.output_list:  # Check if the amplifier has produced output
                        signal = amp.output_list.pop(0)  # Update signal for the next amplifier

            max_signal = max(max_signal, signal)  # Track the maximum signal produced

        return max_signal  # Return the highest signal output


signal_p1 = Intcode_Amplifiers(input_program).run_amplifiers(range(0, 5))
print(f"Part 1: {signal_p1}")

signal_p2= Intcode_Amplifiers(input_program).run_amplifiers(range(5, 10))
print(f"Part 2: {signal_p2}")