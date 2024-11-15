# Advent of Code - Day 11, Year 2017
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2017/day/11
# Solution by: [abbasmoosajee07]
# Brief: [Cardinal Directions]

import os

# Load the input file
D11_file = "Day11_input.txt"
D11_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D11_file)

# Load input data from the specified file path
with open(D11_file_path) as file:
    input_data = file.read().strip().split(",")

def move_on_hex_grid(direction_list):
    # Starting position
    x, y, z = 0, 0, 0
    max_distance = 0  # Track the maximum distance from the origin

    # Move based on directions
    for direction in direction_list:
        if direction == "n":       # North
            y += 1
            z -= 1
        elif direction == "s":     # South
            y -= 1
            z += 1
        elif direction == "ne":    # Northeast
            x += 1
            z -= 1
        elif direction == "se":    # Southeast
            x += 1
            y -= 1
        elif direction == "nw":    # Northwest
            x -= 1
            y += 1
        elif direction == "sw":    # Southwest
            x -= 1
            z += 1
        
        # Calculate the distance from origin
        current_distance = hex_distance(x, y, z)
        max_distance = max(max_distance, current_distance)

    # Return the final position and the maximum distance encountered
    return (x, y, z), max_distance

def hex_distance(x, y, z):
    """Calculate the distance to the origin on a hex grid."""
    return max(abs(x), abs(y), abs(z), abs(x + y + z))

# Run the hex grid movement function
end_point, max_distance_reached = move_on_hex_grid(input_data)

# Calculate the shortest path back to the origin from the endpoint
shortest_distance_back = hex_distance(*end_point)

print("Final position:", end_point)
print("Shortest distance back:", shortest_distance_back)
print("Farthest distance reached:", max_distance_reached)


# 832 too low
# 877, needed to make it 3d so add a z coordinate
#  914 not right, so around it
# 1243 too high
# 1777 too high
