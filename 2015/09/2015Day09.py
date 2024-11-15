# Advent of Code - Day 9, Year 2015
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2015/day/9
# Solution by: [abbasmoosajee07]
# Brief: [Standard Travelling Salesman Problem]

import itertools
import pandas as pd
import os

# Function to parse a line of input
def parse_line(line):
    words = line.strip().split(" ")
    return words[0], words[2], int(words[-1])

# Lookup function for distance
def lookup_dist(start, end, graph):
    if start == end:
        return 0
    return graph.get(start, {}).get(end, 10000)  # Large number for unconnected cities

# Function to calculate all possible routes and their distances
def calculate_routes(graph):
    cities = [city for city in graph.keys() if city != "dummy"]
    all_routes = itertools.permutations(cities, len(cities))

    routes_data = []
    for route in all_routes:
        distance = sum(lookup_dist(route[i], route[i + 1], graph) for i in range(len(route) - 1))
        routes_data.append({"route": " -> ".join(route), "distance": distance})

    return pd.DataFrame(routes_data)

# Main function to read the input and build the graph
def build_graph(file_path):
    graph = {}
    with open(file_path, 'r') as file:
        for line in file:
            start, end, dist = parse_line(line)
            graph.setdefault(start, {})[end] = dist
            graph.setdefault(end, {})[start] = dist

    # Add dummy city for Held-Karp
    graph["dummy"] = {city: 0 for city in graph.keys() if city != "dummy"}
    for city in graph.keys():
        if city != "dummy":
            graph[city]["dummy"] = 0

    return graph

# Define the file path
d9_file = "Day09_input.txt"
d9_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), d9_file)

# Build the graph
graph = build_graph(d9_file_path)

# Calculate all possible routes and their distances
all_routes = calculate_routes(graph)

# Find the shortest and longest routes
min_routes = all_routes[all_routes['distance'] == all_routes['distance'].min()]
max_routes = all_routes[all_routes['distance'] == all_routes['distance'].max()]

print("Shortest Routes:")
print(min_routes)
print("\nLongest Routes:")
print(max_routes)

# Optional: Visualization
# Uncomment below to create a visual representation of routes (requires matplotlib)

# import matplotlib.pyplot as plt
# import networkx as nx

# def plot_routes(graph, routes_df):
#     G = nx.Graph()
#     for start, connections in graph.items():
#         for end, dist in connections.items():
#             if start != "dummy" and end != "dummy":  # Exclude dummy city from plot
#                 G.add_edge(start, end, weight=dist)

#     pos = nx.spring_layout(G)
#     plt.figure(figsize=(10, 8))
#     nx.draw_networkx_nodes(G, pos, node_size=700)
#     nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
#     nx.draw_networkx_labels(G, pos, font_size=12, font_family="sans-serif")

#     plt.title("Graph Representation of Cities and Distances")
#     plt.show()

# plot_routes(graph, all_routes)
