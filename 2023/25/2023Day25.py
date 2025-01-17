"""Advent of Code - Day 25, Year 2023
Solution Started: Jan 17, 2025
Puzzle Link: https://adventofcode.com/2023/day/25
Solution by: abbasmoosajee07
Brief: [Network Wires Graph]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations

# Load the input data from the specified file path
D25_file = "Day25_input.txt"
D25_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D25_file)

# Read and sort input data into a grid
with open(D25_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_input(input_list: list[str]) -> dict:
    wires_dict = {}
    for line in input_list:
        parent, children = line.split(': ')
        wires_dict[parent] = list(children.split(' '))
    return wires_dict

def build_graph(wires_dict: dict):
    # Create a directed graph
    G = nx.Graph()
    count = 0
    # Add edges to the graph
    for parent, children in wires_dict.items():
        for child in children:
            count += 1
            G.add_edge(parent, child, capacity=1)
    return G

def cut_graph(graph):
    for node1, node2 in combinations(graph.nodes, 2):
        cuts, partitions = nx.minimum_cut(graph, node1, node2)
        if cuts == 3:
            break
    return  len(partitions[0]) * len(partitions[1])

wires_dict = parse_input(input_data)
wires_graph = build_graph(wires_dict)
divided_groups = cut_graph(wires_graph)
print("Part 1:", divided_groups)