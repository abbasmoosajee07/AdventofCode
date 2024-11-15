# Advent of Code - Day 15, Year 2015
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2015/day/15
# Solution by: [abbasmoosajee07]
# Brief: [Constrained and Unconstrained Minima Problems]

from sys import path
from itertools import permutations, combinations_with_replacement
import re, os

def parse_ingredients(ingredient_inputs):
    pattern = re.compile(r'(-*\d)')
    return [re.findall(pattern, ingredient) for ingredient in ingredient_inputs]

def ingredient_score(teaspoon_list, ingredient_list):
    combined_list = zip(teaspoon_list, ingredient_list)
    total_ingredients = []
    for multiplication_tuple in combined_list:
        temp_list = [
            int(item) * multiplication_tuple[0] for item in multiplication_tuple[1]
        ]
        total_ingredients.append(temp_list)
    properties = zip(*total_ingredients)
    final_score = 1
    property_count = 1  # this is to ignore calories for part 1
    for cookie_property in properties:
        if sum(cookie_property) > 0:
            final_score *= sum(cookie_property)
        property_count += 1
        if property_count == 5:
            break
    return final_score

def maximize_cookie_score(ingredient_list):
   starting_point = 110 / len(ingredient_list)
   score = 0
   original_teaspoons = [starting_point for ingredient in ingredient_list]
   teaspoons = original_teaspoons.copy()
   amount_to_increase = len(ingredient_list) - 1
   for x in range(0, len(teaspoons)-1):
       while teaspoons[x] <= 100:
           teaspoons[x] += amount_to_increase

def count_calories(teaspoon_list, ingredient_list):
    return sum(
        teaspoon_list[x] * int(ingredient_list[x][-1])
        for x in range(len(ingredient_list))
    )

def brute_force_cookie_score(ingredient_list, max_calorie):
    # Generate ingredient combinations where the sum of teaspoons is 100
    ingredient_combos = [
        element
        for element in permutations(range(1, 100), len(ingredient_list))
        if sum(element) == 100
    ]
    
    max_score = 0
    max_score_with_calories = 0
    
    for ingredient_combination in ingredient_combos:
        # Calculate the score for the current combination
        combo_score = ingredient_score(ingredient_combination, ingredient_list)
        calorie_score = count_calories(ingredient_combination, ingredient_list)
        
        # Update max score without calorie restriction
        if combo_score > max_score:
            max_score = combo_score
        
        # Update max score with calorie restriction of exactly as defined
        if combo_score > max_score_with_calories and calorie_score == max_calorie:
            max_score_with_calories = combo_score
    
    return max_score, max_score_with_calories


D15_file = 'Day15_input.txt'
D15_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D15_file)

with open(D15_file_path) as file:
   input_data = file.read().splitlines()
   
ingredients = parse_ingredients(input_data)
new_max = 500
max_score, max_score_with_calories = brute_force_cookie_score(ingredients, new_max)
print(f"The maximum cookie score is {max_score}")
print(f"The maximum cookie score with {new_max} calories is {max_score_with_calories}")
