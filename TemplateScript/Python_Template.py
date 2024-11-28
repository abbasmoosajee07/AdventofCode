import os
import time

def create_python_script(day=1, year=2024, author='your name',
                            header_text = "Test", repo_dir = ""):
    """
    Sets up the folder structure, Python script, and input file for an Advent of Code challenge.

    Parameters:
        day (int): Day of the challenge.
        year (int): Year of the challenge.
    Returns:
        None
    """
    # Zero-pad the day for folder and filenames
    padded_day = str(day).zfill(2)
    print(repo_dir)
    # Define base directory and paths
    base_dir = os.path.join(repo_dir, str(year), padded_day)
    python_file_path = os.path.join(base_dir, f'{year}Day{padded_day}.py')

    # Ensure the base directory exists
    os.makedirs(base_dir, exist_ok=True)

    # Create Python script if it doesn't already exist
    if not os.path.exists(python_file_path):
        current_time = time.localtime()
        month = time.strftime('%b', current_time)
        script_content = f'''"""{header_text}"""

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the input data from the specified file path
D{padded_day}_file = "Day{padded_day}_input.txt"
D{padded_day}_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D{padded_day}_file)

# Read and sort input data into a grid
with open(D{padded_day}_file_path) as file:
    input_data = file.read().strip().split('\\n')
print(input_data)
'''

        with open(python_file_path, 'w') as python_file:
            python_file.write(script_content)
        print(f"Created Python script '{python_file_path}'.")
    else:
        print(f"Python script '{python_file_path}' already exists.")
