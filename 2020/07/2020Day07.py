# Advent of Code - Day 7, Year 2020
# Solution Started: Nov 20, 2024
# Puzzle Link: https://adventofcode.com/2020/day/7
# Solution by: [abbasmoosajee07]
# Brief: [Bag Sorter and Network Trees]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D07_file = "Day07_input.txt"
D07_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D07_file)

# Read and sort input data into a grid
with open(D07_file_path) as file:
    input_data = file.read().strip().split('\n')

import networkx as nx

def parse_bag_rules(input_data):
    """Parses the input data into a directed graph."""
    graph = nx.DiGraph()  # Directed graph
    for rule in input_data:
        # Split the main bag and contained bags
        main, contains = rule.split('contain')
        main_bag = main.replace('bags', '').replace('bag', '').strip()
        
        if "no other bags" in contains:
            continue  # Skip rules with no contained bags
        
        # Parse each contained bag
        for item in contains.split(','):
            item = item.strip()
            quantity, *bag_name = item.split(' ')
            bag_name = ' '.join(bag_name).replace('bags', '').replace('bag', '').replace('.', '').strip()
            graph.add_edge(main_bag, bag_name, weight=int(quantity))
    
    return graph

def part1_count_containing_bags(graph, target_bag):
    """Counts the number of bag colors that can eventually contain the target bag."""
    reversed_graph = graph.reverse()  # Reverse the graph
    return len(nx.descendants(reversed_graph, target_bag))  # Find all ancestors of the target

def part2_count_total_bags(graph, bag):
    """Counts the total number of individual bags required inside the target bag."""
    total = 0
    for neighbor in graph[bag]:
        quantity = graph[bag][neighbor]['weight']
        total += quantity * (1 + part2_count_total_bags(graph, neighbor))  # Recursive calculation
    return total

# Parse the rules
graph = parse_bag_rules(input_data)

# Solve Part 1
print("Part 1:", part1_count_containing_bags(graph, "shiny gold"))

# Solve Part 2
print("Part 2:", part2_count_total_bags(graph, "shiny gold"))
