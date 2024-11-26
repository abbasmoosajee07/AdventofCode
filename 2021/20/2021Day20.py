# Advent of Code - Day 20, Year 2021
# Solution Started: Nov 26, 2024
# Puzzle Link: https://adventofcode.com/2021/day/20
# Solution by: [abbasmoosajee07]
# Brief: [Code/Problem Description]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
from collections import Counter

# Load the input data from the specified file path
D20_file = "Day20_input.txt"
D20_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D20_file)

# Read and sort input data into a grid
with open(D20_file_path) as file:
    algorithm_raw, image_raw = file.read().strip().split('\n\n')

def decode_image(input_image, algorithm, runs):
    # Parse algorithm into binary mapping
    algo = [1 if char == '#' else 0 for char in algorithm]

    # Convert the input image to a binary numpy array
    image = np.array([[1 if char == '#' else 0 for char in row] for row in input_image], dtype=int)

    for run in range(1, runs + 1):
        # Determine the infinite pixel value for the current run
        infinite_pixel = 1 if algo[0] == 1 and run % 2 == 0 else 0

        # Pad the image with the current infinite pixel value
        expanded_image = np.pad(image, pad_width=2, constant_values=infinite_pixel)

        # Create an empty array for the new enhanced image
        decoded_image = np.zeros((expanded_image.shape[0] - 2, expanded_image.shape[1] - 2), dtype=int)

        # Apply the enhancement algorithm
        for x in range(1, expanded_image.shape[0] - 1):
            for y in range(1, expanded_image.shape[1] - 1):
                # Extract the 3x3 grid and compute the binary index
                sub_grid = expanded_image[x - 1:x + 2, y - 1:y + 2].flatten()
                binary_index = int("".join(map(str, sub_grid)), 2)
                decoded_image[x - 1, y - 1] = algo[binary_index]

        # Update the image for the next run
        image = decoded_image

    # Return the final image and the count of lit pixels
    return image, np.count_nonzero(image)


# Parse input image into a list of strings
input_image = image_raw.split('\n')

# Solve for Part 1
part1_image, ans_p1 = decode_image(input_image, algorithm_raw, runs=2)
print("Part 1:", ans_p1)

# Solve for Part 2
part2_image, ans_p2 = decode_image(input_image, algorithm_raw, runs=50)
print("Part 2:", ans_p2)
