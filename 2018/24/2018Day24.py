# Advent of Code - Day 24, Year 2018
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2018/day/24  # Web link without padding
# Solution by: [abbasmoosajee07]
# Brief: [Infections Vs Immune System Simulation]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D24_file = "Day24_input.txt"
D24_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D24_file)

# Read and sort input data into a grid
with open(D24_file_path) as file:
    input_data = file.read().strip().replace("points with","points () with")

def parse_damage(damage_string):
    damage_type = damage_string[damage_string.rfind(" ") + 1:]
    damage_value = int(damage_string[:damage_string.rfind(" ")])
    return [damage_value if type_ == damage_type else 0 for type_ in types]

def parse_resistances(resistance_string):
    resistance_multipliers = [1, 1, 1, 1, 1]
    
    for resistance in resistance_string.split("; "):
        if len(resistance) == 0:
            continue
            
        multiplier = 1
        if resistance.startswith("weak"):
            multiplier = 2
            resistance = resistance[8:]
        elif resistance.startswith("immune"):
            multiplier = 0
            resistance = resistance[10:]
        
        for damage_type in resistance.split("&"):
            resistance_multipliers[types.index(damage_type)] = multiplier
            
    return resistance_multipliers


def parse_unit_info(unit_info_string):
    unit_info_parts = unit_info_string.split(",")
    damage_info = parse_damage(unit_info_parts[3])
    return [int(unit_info_parts[0]), int(unit_info_parts[1]), parse_resistances(unit_info_parts[2]), damage_info, int(unit_info_parts[4]), 0]

def calculate_damage(attacker, defender):
    return sum(attack * defense for attack, defense in zip(attacker[3], defender[2]))

def run_combat(immune_units, infect_units):
    while len(immune_units) > 0 and len(infect_units) > 0:
        # Update the damage values for both sides based on attack power
        for unit in immune_units:
            unit[-1] = unit[0] * max(unit[3])  # Calculate damage for immune units
        for unit in infect_units:
            unit[-1] = unit[0] * max(unit[3])  # Calculate damage for infect units

        # Sort units by damage (descending), breaking ties by initiative (descending)
        immune_units.sort(key=lambda v: 1000 * (-v[-1]) - v[-2])
        infect_units.sort(key=lambda v: 1000 * (-v[-1]) - v[-2])

        # Determine target selection for immune units
        immune_targets = []
        for immune_unit in immune_units:
            best_target = (0, 100000000, 0, None)
            for idx, infect_unit in enumerate(infect_units):
                if idx in immune_targets:
                    continue
                target_damage = (calculate_damage(immune_unit, infect_unit), infect_unit[-1], infect_unit[-2], idx)
                if target_damage > best_target:
                    best_target = target_damage
            immune_targets.append(best_target[3])

        # Determine target selection for infect units
        infect_targets = []
        for infect_unit in infect_units:
            best_target = (0, 100000000, 0, None)
            for idx, immune_unit in enumerate(immune_units):
                if idx in infect_targets:
                    continue
                target_damage = (calculate_damage(infect_unit, immune_unit), immune_unit[-1], immune_unit[-2], idx)
                if target_damage > best_target:
                    best_target = target_damage
            infect_targets.append(best_target[3])

        # Create a list of all units with type and index for sorting by initiative
        all_units = []
        for idx, immune_unit in enumerate(immune_units):
            all_units.append([0, idx, immune_unit])  # 0 for immune units
        for idx, infect_unit in enumerate(infect_units):
            all_units.append([1, idx, infect_unit])  # 1 for infect units

        all_units.sort(key=lambda v: -v[2][-2])  # Sort by initiative (descending)

        # Track which units are still alive
        alive_immune = immune_units[:]
        alive_infect = infect_units[:]
        total_death_toll = 0

        # Process each unit's attack
        for unit in all_units:
            if unit[0] == 0:  # Immune unit's turn
                if unit[2] not in alive_immune:
                    continue
                if immune_targets[unit[1]] is None:
                    continue
                # Damage calculation and death toll for immune attacking infect
                damage_taken = unit[2][0] * calculate_damage(unit[2], infect_units[immune_targets[unit[1]]])
                death_toll = damage_taken // infect_units[immune_targets[unit[1]]][1]
                infect_units[immune_targets[unit[1]]][0] -= death_toll
                total_death_toll += death_toll
                if infect_units[immune_targets[unit[1]]][0] <= 0:
                    alive_infect.remove(infect_units[immune_targets[unit[1]]])
            else:  # Infect unit's turn
                if unit[2] not in alive_infect:
                    continue
                if infect_targets[unit[1]] is None:
                    continue
                # Damage calculation and death toll for infect attacking immune
                damage_taken = unit[2][0] * calculate_damage(unit[2], immune_units[infect_targets[unit[1]]])
                death_toll = damage_taken // immune_units[infect_targets[unit[1]]][1]
                immune_units[infect_targets[unit[1]]][0] -= death_toll
                total_death_toll += death_toll
                if immune_units[infect_targets[unit[1]]][0] <= 0:
                    alive_immune.remove(immune_units[infect_targets[unit[1]]])

        # If no deaths occur, it's a stalemate
        if total_death_toll == 0:
            return False

        # Update the units that are still alive for the next round
        immune_units = alive_immune
        infect_units = alive_infect

    # Return the total remaining health of the units
    return tuple(sum(v[0] for v in w) for w in [infect_units, immune_units])

def deep_copy(data):
    if isinstance(data, list):
        return [deep_copy(item) for item in data]
    else:
        return data

# List of damage types
types = ['slashing', 'fire', 'bludgeoning', 'radiation', 'cold']

# Clean and parse input data
def clean_unit_data(unit_data):
    """Cleans and formats the raw input data for units."""
    return [
        unit.replace(", ", "&")
            .replace(" units each with ", ",")
            .replace(" hit points (", ",")
            .replace(") with an attack that does ", ",")
            .replace(" damage at initiative ", ",")
        for unit in unit_data.split("\n")[1:]  # Skip header line
    ]

# Parsing input and setting up immune and infect unit data
input_data = input_data.split("\n\n")
immune_data, infect_data = input_data[0], input_data[1]

# Parse the immune and infect units using the clean function
immune_units = list(map(parse_unit_info, clean_unit_data(immune_data)))
infect_units = list(map(parse_unit_info, clean_unit_data(infect_data)))

# Part 1: Run combat without boosting
def part1_combat():
    """Run combat simulation without boosting and return the result."""
    immune_copy = deep_copy(immune_units)
    infect_copy = deep_copy(infect_units)
    return run_combat(immune_copy, infect_copy)[0]

print("Part 1:", part1_combat())

# Part 2: Find optimal boost using binary search
def apply_boost(boost_amount):
    """Apply a boost to immune units and return the result of combat."""
    immune_copy = deep_copy(immune_units)
    infect_copy = deep_copy(infect_units)
    
    # Boost the highest damage value for each immune unit
    for unit in immune_copy:
        max_damage_index = max(enumerate(unit[3]), key=lambda v: v[1])[0]
        unit[3][max_damage_index] += boost_amount
    
    return run_combat(immune_copy, infect_copy)

def find_optimal_boost():
    """Use binary search to find the optimal boost for the immune units."""
    low, high = 1, 100
    while high > low:
        mid = (high + low) // 2
        result = apply_boost(mid)
        if result == False or result[1] == 0:  # If result is invalid or immune has no units left
            low = mid + 1
        else:
            high = mid  # Continue narrowing the range
    return high

# Run the binary search to find the optimal boost for part 2
optimal_boost = find_optimal_boost()
print("Part 2:", apply_boost(optimal_boost)[1])
