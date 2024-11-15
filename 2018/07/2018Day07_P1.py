# Advent of Code - Day 7, Year 2018
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2018/day/7
# Solution by: [abbasmoosajee07]
# Brief: [Kahn's Algorithm Sort]

import os, re
import heapq
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

# Load the input data from the specified file path
D7_file = "Day07_input.txt"
D7_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D7_file)

# Read and sort input data into a grid
with open(D7_file_path) as file:
    input_data = file.read().strip().split('\n')

# Parse the steps from input data
def parse_steps(step_list):
    pattern = r"Step (\w+) must be finished before step (\w+) can begin."
    step_order = []
    for step in step_list:
        match = re.search(pattern, step)
        if match:
            step_order.append((match.group(1), match.group(2)))
    return step_order

# Define the Graph class
class Graph:
    def __init__(self, nodes):
        self.graph = defaultdict(list)
        self.in_degree = defaultdict(int)
        self.nodes = set(nodes)  # Set of all unique nodes
    
    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.in_degree[v] += 1
        if u not in self.in_degree:
            self.in_degree[u] = 0

# Perform topological sorting with alphabetical priority
def alphabetical_kahn_topological_sort(graph):
    queue = [node for node in graph.nodes if graph.in_degree[node] == 0]
    heapq.heapify(queue)
    topological_order = []
    
    while queue:
        node = heapq.heappop(queue)
        topological_order.append(node)
        
        for neighbor in graph.graph[node]:
            graph.in_degree[neighbor] -= 1
            if graph.in_degree[neighbor] == 0:
                heapq.heappush(queue, neighbor)
    
    if len(topological_order) == len(graph.nodes):
        return ''.join(topological_order)
    else:
        return "Graph has at least one cycle"

# Draw a visual representation of the graph
def draw_dependency_graph(edges):
    G = nx.DiGraph()
    G.add_edges_from(edges)

    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue",
            font_size=14, font_weight="bold", arrowsize=20)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): f"{u} -> {v}" for u, v in edges},
                                 font_color="red")
    plt.title("Visual Representation of the Task Dependency Graph")
    # plt.show()

# Example usage

# Parse steps and prepare graph
edges = parse_steps(input_data)
nodes = set(u for u, v in edges).union(v for u, v in edges)
graph = Graph(nodes)
for u, v in edges:
    graph.add_edge(u, v)

# Perform topological sort
topological_order = alphabetical_kahn_topological_sort(graph)
print("Part 1: Topological Order is", topological_order)

# Draw the dependency graph
draw_dependency_graph(edges)
