"""Advent of Code - Day 5, Year 2023
Solution Started: Dec 22, 2024
Puzzle Link: https://adventofcode.com/2023/day/5
Solution by: abbasmoosajee07
Brief: [Creating a gardener's map]
"""

#!/usr/bin/env python3

import os, re, copy,time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

start_time = time.time()
# Load the input data from the specified file path
D05_file = "Day05_input.txt"
D05_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D05_file)

# Read and sort input data into a grid
with open(D05_file_path) as file:
    input_data = file.read().strip().split('\n\n')

def parse_almanac(input_almanac: list) -> tuple[list[int], dict[str, list[dict]]]:
    """
    Parse the input almanac to extract seeds and mapping data.

    Args:
        input_almanac (list): List of strings representing the almanac data.

    Returns:
        tuple: A list of seed values and a dictionary of variable mappings.
    """
    # Parse the seeds from the first line
    seeds = [int(num) for num in input_almanac[0].strip('seeds: ').split(' ')]

    # Initialize the mappings dictionary
    mappings = {}

    for mapping_entry in input_almanac[1:]:
        map_type, mapping_values = mapping_entry.split(' map:\n')
        mapping_list = []

        # Parse rows into a list of dictionaries
        rows = [tuple(map(int, row.split(' '))) for row in mapping_values.split('\n')]
        for dest_start, source_start, range_len in rows:
            mapping_dict = {
                'dest_range': (dest_start, dest_start + range_len),
                'source_range': (source_start, source_start + range_len),
                'range_length': range_len,
            }
            mapping_list.append(mapping_dict)

        # Add the mapping to the dictionary
        mappings[map_type] = mapping_list

    return seeds, mappings

def process_mappings(seed_properties: dict, mappings: dict) -> dict:
    """
    Apply a sequence of mappings to transform seed properties.

    Args:
        seed_properties (dict): Properties of a single seed.
        mappings (dict): Dictionary containing mapping data.

    Returns:
        dict: Updated seed properties after all mappings.
    """
    result_properties = copy.deepcopy(seed_properties)

    # Define the mapping order
    mapping_dict = {
        'seed': 'soil',
        'soil': 'fertilizer',
        'fertilizer': 'water',
        'water': 'light',
        'light': 'temperature',
        'temperature': 'humidity',
        'humidity': 'location'
    }

    for from_type, to_type in mapping_dict.items():
        mapping_key = f"{from_type}-to-{to_type}"
        if mapping_key in mappings:
            result_properties = apply_mapping(
                mappings[mapping_key], result_properties, from_type, to_type
            )

    return result_properties

def apply_mapping(mapping_list: list[dict], seed_properties: dict, from_type: str, to_type: str) -> dict:
    """
    Apply a single mapping transformation to seed properties.

    Args:
        mapping_list (list): List of mapping dictionaries.
        seed_properties (dict): Properties of the seed.
        from_type (str): Source property name.
        to_type (str): Destination property name.

    Returns:
        dict: Updated seed properties after the mapping.
    """
    updated_properties = copy.deepcopy(seed_properties)
    location = seed_properties[from_type]
    mapped = False

    for mapping in mapping_list:
        dest_range = mapping['dest_range']
        source_range = mapping['source_range']

        # Check if the location lies within the source range
        if source_range[0] <= location < source_range[1]:
            shift = dest_range[0] - source_range[0]
            updated_properties[to_type] = location + shift
            mapped = True
            break

    if not mapped:
        # If no mapping applies, retain the same value
        updated_properties[to_type] = location

    return updated_properties

def map_seeds(seed_list: dict, mappings: dict) -> int:
    # Initialize seed properties
    seed_data = {idx + 1: {'seed': seed} for idx, seed in enumerate(seed_list)}

    # Process mappings for each seed
    final_seed_data = {}
    for seed_id, properties in seed_data.items():
        final_seed_data[seed_id] = process_mappings(properties, mappings)

    # # Output the final seed data
    # for seed_id, properties in final_seed_data.items():
    #     print(f"Seed {seed_id}: {properties}")

    # Find the minimum location value
    return min(seed['location'] for seed in final_seed_data.values())

def map_seed_intervals(seeds: list, mappings: dict) -> int:
    """
    Process seed intervals through all mapping levels and find the minimum location.

    Args:
        seeds (list): A list of seeds, where even indices are start values, odd are range lengths.
        segments (list): List of mapping definitions for each level.

    Returns:
        int: The minimum location after applying all mappings.
    """
    # Initialize seed intervals (start, end, level)
    seed_intervals = [
        (seed_start, seed_start + range_len, 0)  # Start at the first level ('seed')
        for seed_start, range_len in zip(seeds[0::2], seeds[1::2])
    ]

    min_location = float('inf')  # Initialize minimum location tracker

    # Define the mapping order
    mapping_order = [
        'seed', 'soil', 'fertilizer', 'water', 'light', 'temperature', 'humidity', 'location'
    ]

    # Process each seed interval through the mappings
    while seed_intervals:
        seed_start, seed_end, level = seed_intervals.pop()

        # If we've reached the final level (location), update the minimum location
        if mapping_order[level] == 'location':  # Final level ('location')
            min_location = min(seed_start, min_location)
            continue

        # Get the current and next mapping levels
        current_level = mapping_order[level]
        next_level = mapping_order[level + 1]
        map_key = f"{current_level}-to-{next_level}"  # Example: "seed-to-soil"

        # Process the mappings for the current level
        for mapping in mappings.get(map_key, []):
            dest_start, dest_end = mapping['dest_range']
            source_start, source_end = mapping['source_range']
            offset = dest_start - source_start

            # Skip intervals with no overlap
            if seed_end <= source_start or source_end <= seed_start:
                continue

            # Handle partial overlap by splitting intervals
            if seed_start < source_start:
                seed_intervals.append((seed_start, source_start, level))
                seed_start = source_start
            if source_end < seed_end:
                seed_intervals.append((source_end, seed_end, level))
                seed_end = source_end

            # Apply the mapping transformation and move to the next level
            seed_intervals.append((seed_start + offset, seed_end + offset, level + 1))
            break  # Only apply the first valid mapping

        else:  # No valid mapping found, pass the interval to the next level unchanged
            seed_intervals.append((seed_start, seed_end, level + 1))

    return min_location

# Parse input data
seeds, mappings = parse_almanac(input_data)

min_loc_p1 = map_seeds(seeds, mappings)
print("Part 1:", min_loc_p1)
min_loc_p2 = map_seed_intervals(seeds, mappings)

print("Part 2:", min_loc_p2) # 17729182
print(time.time() - start_time)
