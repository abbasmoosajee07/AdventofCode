# Advent of Code - Day 22, Year 2017
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2017/day/22
# Solution by: [abbasmoosajee07]
# Brief: [Virus Carrier Simulation, Game of Life]

import os

# Load the input data from the specified file path
D22_file = "Day22_input.txt"
D22_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D22_file)

with open(D22_file_path) as file:
    input_data = file.read().strip().splitlines()

# Function to create the initial grid and set infected nodes
def create_virus_grid(input_data):
    offset = len(input_data) // 2  # Calculate the offset to center the grid
    infected = set()
    
    # Populate the infected set with the coordinates of infected nodes
    for r, line in enumerate(input_data):
        for c, ch in enumerate(line):
            if ch == '#':
                infected.add((r - offset, c - offset))
    return infected

# Part 1 Logic
def virus_spread(total_bursts = 10000):
    # Initialize infected nodes and direction settings
    infected_nodes = create_virus_grid(input_data)
    dirs = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # Directions: up, left, down, right
    current_direction = 0  # Start facing "up"
    virus_position = (0, 0)  # Virus starts at the center of the grid

    # Part 1 Burst Function
    def burst():
        nonlocal infected_nodes, current_direction, virus_position
        infection_caused = False
        
        # If the current node is infected
        if virus_position in infected_nodes:
            current_direction = (current_direction - 1) % 4  # Turn left
            infected_nodes.remove(virus_position)  # Clean the node
        else:  # If the current node is clean
            current_direction = (current_direction + 1) % 4  # Turn right
            infected_nodes.add(virus_position)  # Infect the node
            infection_caused = True
        
        # Move the virus forward in the current direction
        virus_position = (virus_position[0] + dirs[current_direction][0],
                          virus_position[1] + dirs[current_direction][1])
        return infection_caused

    # Total bursts to simulate for Part 1
    num_infections = 0

    # Perform the bursts for Part 1
    for _ in range(total_bursts):
        if burst():
            num_infections += 1  # Count the infections

    # Output the total number of infections caused by the virus for Part 1
    print("Total infections caused (Part 1):", num_infections)

# Part 2 Logic
def virus_evolves(total_bursts = 10000000):
    # Initialize infected nodes and direction settings
    infected_nodes = create_virus_grid(input_data)
    dirs = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # Directions: up, left, down, right
    current_direction = 0  # Start facing "up"
    virus_position = (0, 0)  # Virus starts at the center of the grid

    # Define states
    CLEAN = 0
    INFECTED = 1
    WEAK = 2
    FLAGGED = 3

    # Initialize the state of each node
    state = {k: INFECTED for k in infected_nodes}  # All infected nodes start as INFECTED

    # Part 2 Burst Function
    def burst():
        nonlocal state, current_direction, virus_position
        infection_caused = False
        
        # Get the current state of the virus position
        current_state = state.get(virus_position, CLEAN)
        
        if current_state == CLEAN:  # If the node is clean
            current_direction = (current_direction + 1) % 4  # Turn right
            state[virus_position] = WEAK  # Mark the node as WEAK
        elif current_state == WEAK:  # If the node is weak
            state[virus_position] = INFECTED  # Infect the node
            infection_caused = True  # Infection caused
        elif current_state == INFECTED:  # If the node is infected
            current_direction = (current_direction - 1) % 4  # Turn left
            state[virus_position] = FLAGGED  # Mark the node as FLAGGED
        else:  # If the node is flagged
            current_direction = (current_direction + 2) % 4  # Turn around
            del state[virus_position]  # Remove the node from the state
        
        # Move the virus forward in the current direction
        virus_position = (virus_position[0] + dirs[current_direction][0],
                          virus_position[1] + dirs[current_direction][1])
        return infection_caused

    # Total bursts to simulate for Part 2
    num_infections = 0

    # Perform the bursts for Part 2
    for _ in range(total_bursts):
        if burst():
            num_infections += 1  # Count the infections

    # Output the total number of infections caused by the virus for Part 2
    print("Total infections caused (Part 2):", num_infections)

# Execute both parts
if __name__ == "__main__":
    virus_spread()
    virus_evolves()
