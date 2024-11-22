# Advent of Code - Day 21, Year 2020
# Solution Started: Nov 22, 2024
# Puzzle Link: https://adventofcode.com/2020/day/21
# Solution by: [abbasmoosajee07]
# Brief: [Allergens and ingredients]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D21_file = "Day21_input.txt"
D21_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D21_file)

# Read and sort input data into a grid
with open(D21_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse(line):
    # Split the line into ingredients and allergens
    ingredients_part, allergens_part = line[:-1].split(" (contains")
    
    # Clean and split the ingredients and allergens into sets
    ingredients = set(ingredients_part.split())
    allergens = set(allergens_part.replace(" ", "").split(","))
    
    return ingredients, allergens

# Parse each line and group by ingredients and allergens
parsed_data = [parse(line) for line in input_data]

# Unzip the parsed data into two separate lists: all ingredients and all allergens
ingredient_sets, allergen_sets = zip(*parsed_data)

# Get all unique ingredients and allergens
all_ingredients = set.union(*ingredient_sets)
all_allergens = set.union(*allergen_sets)

# Map allergens to their possible ingredients
allergen_to_possible_ingredients = {
    allergen: set.intersection(*[ingredients for ingredients, allergens in zip(ingredient_sets, allergen_sets) if allergen in allergens])
    for allergen in all_allergens
}

# Identify allergen-ingredient pairs, reducing possibilities as we go
allergen_ingredient_pairs = []

while allergen_to_possible_ingredients:
    # Find the allergen with only one possible ingredient
    allergen, possible_ingredients = next(
        (key, value) for key, value in allergen_to_possible_ingredients.items() if len(value) == 1
    )
    
    # Add the allergen-ingredient pair and remove it from other allergen possibilities
    ingredient = list(possible_ingredients)[0]
    allergen_ingredient_pairs.append((allergen, ingredient))
    del allergen_to_possible_ingredients[allergen]
    
    # Remove the identified ingredient from other allergen sets
    for remaining_ingredients in allergen_to_possible_ingredients.values():
        remaining_ingredients.discard(ingredient)

# Get the free ingredients (those not associated with any allergen)
_, free_ingredients = zip(*sorted(allergen_ingredient_pairs))

# Identify the ingredients that could contain allergens
allergenic_ingredients = all_ingredients - set(free_ingredients)

# Part 1: Count how many times allergenic ingredients appear in the food lists
ans_p1 = sum(
    sum(1 for ingredient in food if ingredient in allergenic_ingredients) for food in ingredient_sets
)

# Part 2: Return the list of free ingredients associated with allergens, sorted alphabetically
ans_p2 = ",".join(free_ingredients)


# Print the results
print("Part 1:", ans_p1)  # Part 1 result
print("Part 2:", ans_p2)  # Part 2 result
