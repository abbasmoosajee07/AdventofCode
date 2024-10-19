import os
import re
import numpy as np

# Define the input file path
D10_file = 'Day10_input.txt'
D10_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D10_file)

# Read input file
with open(D10_file_path) as file:
    input_lines = file.read().splitlines()
    
print(input_lines)