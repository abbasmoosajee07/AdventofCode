import os
import re
import numpy as np

# Define the input file path
D8_file = 'Day8_input.txt'
D8_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D8_file)

# Read input file
with open(D8_file_path) as file:
    input_lines = file.read().splitlines()
    
light_matrix = np.zeros((6, 50)) 

instruction = input_lines[0]


if __name__ == "__main__":
    print(light_matrix)