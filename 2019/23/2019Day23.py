"""Advent of Code - Day 23, Year 2019
Solution Started: Mar 12, 2025
Puzzle Link: https://adventofcode.com/2019/day/23
Solution by: abbasmoosajee07
Brief: [Intcode Networks]
"""

#!/usr/bin/env python3

import os, re, copy, time, sys
start_time = time.time()

intcode_path = os.path.join(os.path.dirname(__file__), "..", "Intcode_Computer")
sys.path.append(intcode_path)
# from Intcode_Computer import Intcode_CPU

# Load the input data from the specified file path
D23_file = "Day23_input.txt"
D23_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D23_file)

# Read and sort input data into a grid
with open(D23_file_path) as file:
    input_data = file.read().strip().split(',')
    input_program = [int(num) for num in input_data]

class Intcode_Networks:
    NETWORK_SIZE = 50  # Number of computers in the network

    def __init__(self, program):
        """
        Initialize a network of 50 Intcode computers.
        Each computer starts with a unique ID (0-49) and the provided Intcode program.
        """
        from Intcode_Computer import Intcode_CPU
        self.computers = {i: Intcode_CPU(program.copy(), [i]) for i in range(self.NETWORK_SIZE)}
        self.queues = {i: [] for i in range(self.NETWORK_SIZE)}

    def run_network(self):
        """
        Run the network of computers continuously. Each computer processes its input,
        sends outputs to other computers, and checks for special 'destination 255' outputs.
        The network will terminate when a packet is sent to destination 255, returning its Y value.
        """
        while True:
            idle = True  # Assume idle until proven otherwise

            for comp_no in range(self.NETWORK_SIZE):
                # Process the computer, either with its input queue or -1 if no input
                if self.queues[comp_no]:
                    self.computers[comp_no].process_program(self.queues[comp_no])
                    self.queues[comp_no].clear()  # Clear the input queue after processing
                    idle = False  # Activity detected, network is not idle
                else:
                    self.computers[comp_no].process_program([-1])  # No input, send -1

                # Clear paused state and get output from the computer
                self.computers[comp_no].paused = False
                output = self.computers[comp_no].get_result("output")
                self.computers[comp_no].output_list = []  # Clear output list after processing

                # Process output in chunks of three (dest, x, y)
                for pos in range(0, len(output), 3):
                    dest, x, y = output[pos:pos + 3]
                    if dest == 255:
                        return y  # Return the Y value if destination is 255
                    self.queues[dest].extend([x, y])  # Forward the packet to the correct queue
                    idle = False  # A packet was sent, network is not idle

            # If the network is idle (no packets sent or received), log the idle state
            if idle:
                print("Network is idle.")


# Run the network
network = Intcode_Networks(input_program)
part1_result = network.run_network()

print("Part 1:", part1_result)
print(f"Execution Time = {time.time() - start_time:.5f}s")
