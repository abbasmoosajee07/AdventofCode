# Advent of Code - Day 12, Year 2017
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2017/day/12
# Solution by: [abbasmoosajee07]
# Brief: [Linked Numbers and Graphs]

import os
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

# Load the input file
D12_file = "Day12_input.txt"
D12_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D12_file)

# Load input data from the specified file path
with open(D12_file_path) as file:
    input_data = file.read().strip().split("\n")

# Create the graph
graph = nx.Graph()

for line in input_data:
    # Parse the line
    node, neighbors = line.split(" <-> ")
    node = int(node)  # Convert node to an integer for simplicity
    neighbors = [int(neighbor) for neighbor in neighbors.split(", ")]
    
    # Add edges defined by this line
    graph.add_edges_from((node, neighbor) for neighbor in neighbors)

# Part 1: Size of the component containing node '0'
contain_no = 0
print(f'Part 1: Goups containing No {contain_no}', len(nx.node_connected_component(graph, contain_no)))

# Part 2: Total number of connected components
print('Part 2: Total number of Groups', nx.number_connected_components(graph))

# Calculate node degrees (frequency of connections)
node_degrees = dict(graph.degree())

# Normalize degree values for color mapping
degree_values = np.array(list(node_degrees.values()))
norm = plt.Normalize(vmin=degree_values.min(), vmax=degree_values.max())
cmap = cm.viridis  # Define the colormap

# Map each node to its color based on frequency
node_colors = [cmap(norm(degree)) for degree in degree_values]

# Create the plot and draw the graph with colored nodes
fig, ax = plt.subplots(figsize=(10, 8))
pos = nx.spring_layout(graph)  # Define the layout for the graph

# Draw nodes with labels and edges, colored by degree frequency
nx.draw(graph, pos, with_labels=True, node_size=200, node_color=node_colors,
        font_size=10, font_weight="bold", edge_color="gray", ax=ax)

# Set the title
plt.title("Visual Representation of Program Connections with Node Colors by Frequency")

# Create the color bar using ScalarMappable, linked to the color map and norm
sm = cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
fig.colorbar(sm, ax=ax, label="Connection Frequency (Degree)")

# plt.show()
