"""Advent of Code - Day 14, Year 2019
Solution Started: Jan 25, 2025
Puzzle Link: https://adventofcode.com/2019/day/14
Solution by: abbasmoosajee07
Brief: [Reactions and Golden Search]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D14_file = "Day14_input.txt"
D14_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D14_file)

# Read and sort input data into a grid
with open(D14_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_input(input_reactions: list[str]) -> dict:
    reaction_dict = {}
    for line in input_reactions:
        reactants, products = line.split(' => ')

        # Parse the reactants and products
        reactant_list = [(int(num), name) for reac in reactants.split(',') for num, name in [reac.split()]]
        product_list = [(int(num), name) for prod in products.split(',') for num, name in [prod.split()]]

        # Store the reaction in the dictionary
        if len(product_list) >= 2:
            raise ValueError("More than one product produced in reaction")
        else:
            # reaction_dict[tuple(reactant_list)] = product_list[0]  # Use tuple instead of list as the key
            reaction_dict[product_list[0][1]] = (product_list[0][0], tuple(reactant_list))  # Use tuple instead of list as the key

    return reaction_dict

def calc_required_ore(reaction_dict: dict, final_product: tuple = (1, 'FUEL')) -> dict:
    """
    Calculates the amount of ORE required to produce a given quantity of the final product (e.g., FUEL).
    Assumes reaction_dict contains all reactions.
    """
    required = {'ORE': 0}  # Tracks how much of each resource is required
    produced = {product: 0 for product in reaction_dict.keys()}  # Tracks how much is produced
    required[final_product[1]] = final_product[0]  # Initialize with the desired product and quantity

    # Continue production until all requirements are satisfied
    while True:
        if not any(qty > produced[prod] for prod, qty in required.items() if prod != 'ORE'):
            break
        for product, needed_qty in list(required.items()):
            # print(product, needed_qty)
            # Skip if we've produced enough of this product
            if product == 'ORE' or needed_qty <= produced[product]:
                continue

            # Calculate how many batches we need to meet the required quantity
            prod_qty, reactants = reaction_dict[product]
            remaining_qty = needed_qty - produced[product] # Quantiity required
            batches = -(-remaining_qty // prod_qty)  # Ceiling division

            # Produce the product
            produced[product] += batches * prod_qty

            # Update the required quantities of reactants
            for react_qty, reactant in reactants:
                if reactant not in required:
                    required[reactant] = 0
                required[reactant] += react_qty * batches

    return required

def calc_produced_fuel(reaction_dict: dict, available_ore: int) -> int:
    """
    Uses binary search to find the maximum amount of FUEL that can be produced with the given amount of ORE.
    """
    low = 1
    high = available_ore ** 2 # Start with an arbitrary large upper bound
    max_fuel = 0

    while low <= high:

        mid = (low + high) // 2
        ore_needed = calc_required_ore(reaction_dict, final_product=(mid, 'FUEL'))['ORE']

        if ore_needed > available_ore:
            high = mid - 1  # Reduce search space
        else:
            max_fuel = mid  # Update maximum FUEL found
            low = mid + 1  # Increase search space for more FUEL

    return max_fuel

parsed_reactions = parse_input(input_data)

# Calculate the required reactants for the desired product ('FUEL' in this case)
required_reactants = calc_required_ore(parsed_reactions)
print("Part 1:", required_reactants['ORE'])

available_ore = 1_000_000_000_000  # 1 trillion ORE
fuel_prod = calc_produced_fuel(parsed_reactions, available_ore)
print("Part 2:", fuel_prod)
