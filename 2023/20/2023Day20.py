"""Advent of Code - Day 20, Year 2023
Solution Started: Jan 9, 2025
Puzzle Link: https://adventofcode.com/2023/day/20
Solution by: abbasmoosajee07
Brief: [Sending and Recieving Pulses]
"""

#!/usr/bin/env python3

import os, re, copy, math
from itertools import count
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D20_file = "Day20_input.txt"
D20_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D20_file)

# Read and sort input data into a grid
with open(D20_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_input(input_list: list[str]) -> tuple[dict, list]:
    graph, flip_flop, memory = {}, {}, {}
    for line in input_list:
        source, destinations = line.split(' -> ')
        destinations = destinations.split(', ')
        graph[source.strip('%&')] = destinations
        if source.startswith('%'):
            flip_flop[source[1:]] = 0   # each flip flip is off (0) by default
        elif source.startswith('&'):
            memory[source[1:]] = {}

    for conjunction in memory.keys():   # get source modules for conjunctions
        for source, destinatons in graph.items():
            if conjunction in destinatons:
                memory[conjunction][source] = 0   # initialize memory at low (0)
    return graph, flip_flop, memory

def send_pulses(modules_graph: dict, flip_flop: dict, memory: dict, total_press: int = 1000):
    def press_buttons(buttons_queue: list):
        while buttons_queue:
            out_module, in_module, pulse = buttons_queue.pop(0)
            pulse_count[pulse] += 1

            if in_module in flip_flop and pulse == 0:
                flip_flop[in_module] = 1 - flip_flop[in_module]
                out_pulse = flip_flop[in_module]

            elif in_module in memory:
                memory[in_module][out_module] = pulse
                out_pulse = 1 if 0 in memory[in_module].values() else 0

            else:   # no output
                continue

            buttons_queue.extend([(in_module, nxt, out_pulse) for nxt in modules_graph[in_module]])
    flip_flop = copy.deepcopy(flip_flop)
    pulse_count = [0, 0]       # [low, high]
    for steps in range(total_press):
        pulse_count[0] += 1    # initial low signal from button to broadcaster
        queue = [('broadcaster', in_module, 0) for in_module in modules_graph['broadcaster']]
        press_buttons(queue)
        # print(f"{steps=} {signal_count=}")
    return pulse_count

def min_pulses_required(modules_graph: dict, flip_flop: dict, memory: dict):
    flip_flop = copy.deepcopy(flip_flop)
    final_layer = [module for module in modules_graph.keys() if 'rx' in modules_graph[module]]
    assert len(final_layer) == 1, "Assumption #1: There is only 1 module pointing to rx"
    assert final_layer[0] in memory, "Assumption #2: The final module before rx is a conjunction"

    semi_final_layer = set(module for module in modules_graph if final_layer[0] in modules_graph[module])
    cycle_lengths = []  # Assumption #3: The modules on semi_final_layer signal high in regular intervals / cycles

    for button_push in count(1):
        buttons_queue = [('broadcaster', in_module, 0) for in_module in modules_graph['broadcaster']]
        while buttons_queue:
            out_module, in_module, pulse = buttons_queue.pop(0)

            if in_module in flip_flop and pulse == 0:
                flip_flop[in_module] = 1 - flip_flop[in_module]
                out_pulse = flip_flop[in_module]

            elif in_module in memory:
                memory[in_module][out_module] = pulse
                out_pulse = 1 if 0 in memory[in_module].values() else 0
                if in_module in semi_final_layer and out_pulse == 1:
                    cycle_lengths.append(button_push)
                    semi_final_layer.remove(in_module)

            else:   # no output
                continue

            buttons_queue.extend([(in_module, nxt, out_pulse) for nxt in modules_graph[in_module]])

        if not semi_final_layer:
            break

    return cycle_lengths

modules_dict, flip_flop, memory = parse_input(input_data)

press_count = send_pulses(modules_dict, flip_flop, memory)
print("Part 1:", press_count[0] * press_count[1])

reqd_press = min_pulses_required(modules_dict, flip_flop, memory)
print("Part 2:", math.lcm(*reqd_press))
