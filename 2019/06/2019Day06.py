# Advent of Code - Day 6, Year 2019
# Solution Started: Nov 17, 2024
# Puzzle Link: https://adventofcode.com/2019/day/6
# Solution by: [abbasmoosajee07]
# Brief: [Orbiting Objects]

#!/usr/bin/env python3

import os, re, copy
import networkx as nx
from typing import List

# Load the input data from the specified file path
D06_file = "Day06_input.txt"
D06_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D06_file)

# Read and sort input data into a grid
with open(D06_file_path) as file:
    input_data = file.read().strip().split('\n')

def to_graph(lines: List[str], Directed = False):
    if Directed:
        graph = nx.Graph()
    else:
        graph = nx.DiGraph()

    for line in lines:
        parent, child = line.strip().split(")")
        graph.add_edge(parent, child)
    return graph

def total_orbits(graph: nx.DiGraph) -> int:
    # Compute the total number of direct and indirect orbits
    total = 0
    for node in graph.nodes:
        total += len(nx.ancestors(graph, node))  # Ancestors represent all indirect orbits
    return total

def orbital_transfers(graph: nx.Graph, start: str, end: str) -> int:
    # Find the shortest path length from the node orbiting YOU to the node orbiting SAN
    start_orbit = list(graph.neighbors(start))[0]
    end_orbit = list(graph.neighbors(end))[0]
    return nx.shortest_path_length(graph, start_orbit, end_orbit)

graph_p1 = to_graph(input_data)
ans_p1 = total_orbits(graph_p1)
print(f"Part 1: {ans_p1}")

undirected_graph_p2 = to_graph(input_data, True)
ans_p2 = orbital_transfers(undirected_graph_p2, "YOU", "SAN")
print(f"Part 2: {ans_p2}")