"""Advent of Code - Day 23, Year 2024
Solution Started: Dec 23, 2024
Puzzle Link: https://adventofcode.com/2024/day/23
Solution by: abbasmoosajee07
Brief: [Computer Networks]
"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D23_file = "Day23_input.txt"
D23_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D23_file)

# Read and sort input data into a grid
with open(D23_file_path) as file:
    input_data = file.read().strip().split('\n')

def build_graph(node_list: list[str]):
    # Create a network graph
    G = nx.Graph()

    # Loop to add nodes and edges
    for pair in node_list:
        parent, child = pair.split('-')
        G.add_node(parent)  # Add parent node
        G.add_node(child)   # Add child node
        G.add_edge(parent, child)  # Add directed edge from parent to child
    return G

def nodes_with_computer(Graph, contains: str, node_len: int):
    node_list = list(nx.enumerate_all_cliques(Graph))
    computer_count = 0
    for triangle in node_list:
        if len(triangle) == node_len:
            if any(computer.startswith(contains) for computer in triangle):
                computer_count += 1
    return computer_count

def find_password(graph):
    # Find all cliques in the undirected graph
    cliques = list(nx.find_cliques(graph))

    # Find the largest clique
    largest_clique = max(cliques, key=len)

    # Sort the names of the computers in the largest clique alphabetically
    sorted_computers = sorted(largest_clique)

    # Generate the password by joining the sorted computer names with commas
    password = ','.join(sorted_computers)
    return password

node_graph = build_graph(input_data)

ans_p1 = nodes_with_computer(node_graph, 't', 3)
print("Part 1:", ans_p1)


ans_p2 = find_password(node_graph)
print("Part 2:", ans_p2)
