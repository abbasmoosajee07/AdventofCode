"""Advent of Code - Day 5, Year 2023
Solution Started: Dec 22, 2024
Puzzle Link: https://adventofcode.com/2023/day/5
Solution by: abbasmoosajee07
Brief: [Creating a gardener's map]
299285429 too low
2448156885 too high
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D05_file = "Day05_input.txt"
D05_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D05_file)

# Read and sort input data into a grid
with open(D05_file_path) as file:
    input_data = file.read().strip().split('\n\n')

def parse_almanac(input_almanac: list) -> tuple[list[int], dict[list]]:
    # Parse the seeds from the first line
    seeds = {idx + 1: {'seed': int(num)} for idx, num in enumerate(input_almanac[0].strip('seeds: ').split(' '))}

    # Initialize the map dictionary
    map_dict = {}

    for variable_map in input_almanac[1:]:
        map_type, values = variable_map.split(' map:\n')
        loc_list = []

        # Parse the rows and create a list of tuples (dest_start, source_start, range_len)
        row_list = [tuple(map(int, row.split(' '))) for row in values.split('\n')]

        # Sort the rows based on the dest_start value (index 0 of each tuple)
        sorted_rows = sorted(row_list, key=lambda x: (x[0], x[1]))

        # Create loc_dict from the sorted rows
        for row in row_list:
            dest_start, source_start, range_len = row
            loc_dict = {
                'dest': (dest_start, dest_start + range_len - 1),
                'source': (source_start, source_start + range_len - 1),
                'range': range_len,
            }
            loc_list.append(loc_dict)

        # Add the map to the dictionary
        map_dict[map_type] = loc_list

    return seeds, map_dict

def process_mappings(seed_dict: dict, variables_map: dict) -> dict:
    result_dict = copy.deepcopy(seed_dict)
    # Define the mapping order as a list of tuples
    mapping_dict = {
        'seed': 'soil',
        'soil': 'fertilizer',
        'fertilizer': 'water',
        'water': 'light',
        'light': 'temperature',
        'temperature': 'humidity',
        'humidity': 'location'
    }
    # Process each mapping transformation in order
    for from_loc, to_loc in mapping_dict.items():
        if from_loc + '-to-' + to_loc in variables_map:
            result_dict = map_locations(
                variables_map[from_loc + '-to-' + to_loc],
                result_dict,
                from_loc,
                to_loc
            )
    return result_dict

def find_min_prop(seed_dict: dict, target_prop:str ='location') -> int:
    min_prop = float('inf')
    for no, seed_props in seed_dict.items():
        prop = seed_props[target_prop]
        min_prop = min(min_prop, prop)
    return min_prop

def map_locations(variables_map: list[dict], seed_dict: dict, from_loc: str, to_loc: str) -> dict:

    dict_copy = copy.deepcopy(seed_dict)

    # Process each seed in the seed list
    for seed_no, seed_props in seed_dict.items():
        location = seed_props[from_loc]
        mapped = False  # Track if the seed was mapped
        total_range = 0

        for test_map in variables_map:
            dest_range = test_map['dest']
            source_range = test_map['source']
            range_len = test_map['range']

            # Check if the seed lies within the current dest range
            if source_range[0] <= location <= source_range[1]:
                diff_shift = dest_range[0] - source_range[0]
                target_loc = location + diff_shift # Map to the corresponding source
                # print(f"{location=} {dest_range=} {source_range=} {range_len=} {target_loc=}")
                dict_copy[seed_no][to_loc] = target_loc
                mapped = True
                break  # Stop once the seed is mapped
            total_range += range_len
        # If seed is not found in any range, map it to itself
        if not mapped:
            dict_copy[seed_no][to_loc] = location  # Assign the seed itself

    return dict_copy

test_input = ['seeds: 79 14 55 13',
                'seed-to-soil map:\n50 98 2\n52 50 48',
                'soil-to-fertilizer map:\n0 15 37\n37 52 2\n39 0 15',
                'fertilizer-to-water map:\n49 53 8\n0 11 42\n42 0 7\n57 7 4',
                'water-to-light map:\n88 18 7\n18 25 70',
                'light-to-temperature map:\n45 77 23\n81 45 19\n68 64 13',
                'temperature-to-humidity map:\n0 69 1\n1 0 69',
                'humidity-to-location map:\n60 56 37\n56 93 4']

seeds_dict, variables_map = parse_almanac(input_data)
print(variables_map)

# Process all mappings
seed_dict_final = process_mappings(seeds_dict, variables_map)

min_loc = find_min_prop(seed_dict_final)
print("Part 1:", min_loc)

for no, props in seed_dict_final.items():
    print(f"{no=} {props}")
print()

