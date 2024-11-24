# Advent of Code - Day 12, Year 2021
# Solution Started: Nov 24, 2024
# Puzzle Link: https://adventofcode.com/2021/day/12
# Solution by: [abbasmoosajee07]
# Brief: [Cave Path Finding]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D12_file = "Day12_input.txt"
D12_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D12_file)

# Read and sort input data into a grid
with open(D12_file_path) as file:
    input_data = file.read().strip().split('\n')

def map_network(input, show):
    connection_list = [connections.split('-') for connections in input]

    # Create an undirected graph
    G = nx.Graph()

    for connection in connection_list:
        # Add edges between nodes (this also adds nodes automatically if they don't exist)
        G.add_edges_from([connection])
    
    if show:
        # Draw the graph
        nx.draw(G, with_labels=True, node_color='lightblue', node_size=500, font_size=12)

        # Display the graph
        plt.show()

    return G

def find_paths_part_v1(G, current_node, visited, path):
    # Base case: Reached the end
    if current_node == 'end':
        return [path]

    paths = []
    for neighbor in G[current_node]:
        if neighbor.islower() and neighbor in visited:
            continue  # Skip small caves already visited
        paths += find_paths_part_v1(G, neighbor, visited | {neighbor}, path + [neighbor])

    return paths

start_point = 'start'
network_graph = map_network(input_data, show=False)
paths = find_paths_part_v1(network_graph, start_point, {start_point}, [start_point])
print("Part 1:", len(paths))

def find_paths_part_v2(G, current_node, visited, path, visited_twice):
    # Base case: Reached the end
    if current_node == 'end':
        return [path]

    paths = []
    for neighbor in G[current_node]:
        if neighbor == start_point:
            continue  # Never revisit the start_point node
        if neighbor.islower() and neighbor in visited:
            if visited_twice:
                continue  # Skip if we've already visited a small cave twice
            else:
                # Allow this small cave to be visited a second time
                paths += find_paths_part_v2(G, neighbor, visited, path + [neighbor], True)
        else:
            # Continue with the normal rules
            paths += find_paths_part_v2(G, neighbor, visited | {neighbor}, path + [neighbor], visited_twice)

    return paths

paths = find_paths_part_v2(network_graph, start_point, {start_point}, [start_point], False)
print("Part 2:", len(paths))
