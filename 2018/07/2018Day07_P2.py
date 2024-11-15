# Advent of Code - Day 7, Year 2018
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2018/day/7
# Solution by: [abbasmoosajee07]
# Brief: [Scheduling Workers based on lexicographical topological sort]

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


def parse_steps(step_list):
    pattern = r"Step (\w+) must be finished before step (\w+) can begin."
    step_order = []
    for step in step_list:
        match = re.search(pattern, step)
        if match:
            step_order.append((match.group(1), match.group(2)))
    return step_order

class Graph:
    def __init__(self, nodes):
        self.graph = defaultdict(list)
        self.in_degree = defaultdict(int)
        self.nodes = set(nodes)
    
    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.in_degree[v] += 1
        if u not in self.in_degree:
            self.in_degree[u] = 0

def calculate_step_duration(step, base_time=0):
    return base_time + (ord(step) - ord('A') + 1)

def simulate_workers(graph, edges, num_workers, base_time):
    # Initialize graph dependencies
    for u, v in edges:
        graph.add_edge(u, v)

    # Priority queue for available steps (alphabetical order)
    available_steps = [node for node in graph.nodes if graph.in_degree[node] == 0]
    heapq.heapify(available_steps)

    # Tracking workers' current tasks and remaining time
    workers = [None] * num_workers  # None represents an idle worker
    worker_times = [0] * num_workers
    time = 0
    completed_steps = []

    while available_steps or any(workers):
        # Assign steps to idle workers
        for i in range(num_workers):
            if workers[i] is None and available_steps:
                next_step = heapq.heappop(available_steps)
                workers[i] = next_step
                worker_times[i] = calculate_step_duration(next_step, base_time)

        # Simulate passage of time by 1 second
        time += 1
        for i in range(num_workers):
            if workers[i] is not None:
                worker_times[i] -= 1
                # Check if a worker has completed a task
                if worker_times[i] == 0:
                    finished_step = workers[i]
                    completed_steps.append(finished_step)
                    workers[i] = None  # Set worker as idle
                    # Update dependencies of finished task
                    for dependent in graph.graph[finished_step]:
                        graph.in_degree[dependent] -= 1
                        if graph.in_degree[dependent] == 0:
                            heapq.heappush(available_steps, dependent)

    return time, "".join(completed_steps)

# Example usage

# Parse input, create graph, and calculate time
edges = parse_steps(input_data)
nodes = set(u for u, v in edges).union(v for u, v in edges)
graph = Graph(nodes)
num_workers = 5
base_time = 60  # for simplified example where base time is reduced by 60

# Simulate the worker process
total_time, order = simulate_workers(graph, edges, num_workers, base_time)

print("Total Time to Complete All Steps:", total_time)
print("Order of Steps Completed:", order)
