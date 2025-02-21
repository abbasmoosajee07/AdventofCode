"""Advent of Code - Day 23, Year 2019
Solution Started: Feb 17, 2025
Puzzle Link: https://adventofcode.com/2019/day/23
Solution by: abbasmoosajee07
Brief: [Intcode Networks]
"""

#!/usr/bin/env python3

import os, re, copy, time, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
    NETWORK_SIZE = 50

    def __init__(self, NIC_SOFTWARE: list[int]):
        self.software = NIC_SOFTWARE
        from Intcode_Computer import Intcode_CPU
        self.computer = Intcode_CPU(NIC_SOFTWARE)

    def build_network(self, visualize: bool = False):
        comp_list = list(range(self.NETWORK_SIZE))
        comps_reached = []
        queue = comp_list.copy()
        cpu_input = [0, -1]
        while queue:
            num = queue.pop(0)
            print("in", cpu_input)
            node = self.computer.replicate()
            node.process_program(cpu_input)

            node.paused = False
            output = node.get_result("output")
            if len(output) == 0:
                cpu_input = [num, -1]
            else:
                comp_list.remove(cpu_input[0])
                comps_reached.append(cpu_input[0])
                cpu_input = output[:3]

            if 255 in output:
                print("final", output)
                break

            if visualize:
                print("out", output)

        print(comp_list)
        print(comps_reached)
        return 0

networks = Intcode_Networks(input_program)

addr_y = networks.build_network(True)
print("Part 1:", addr_y)

print(f"Execution Time = {time.time() - start_time:.5f}s")
