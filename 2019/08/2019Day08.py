# Advent of Code - Day 8, Year 2019
# Solution Started: Nov 17, 2024
# Puzzle Link: https://adventofcode.com/2019/day/8
# Solution by: [abbasmoosajee07]
# Brief: [Code/Problem Description]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Load the input data from the specified file path
D08_file = "Day08_input.txt"
D08_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D08_file)

# Read and sort input data into a grid
with open(D08_file_path) as file:
    input_data = file.read().strip().split('\n')
    input_list = list(input_data[0])

size = [25, 6]
image_size = int(np.prod(size))
image_list = []
image_props = []

for pos in range(0, len(input_list), image_size):
    image_n = input_list[pos:pos+image_size]
    zero_count = dict(Counter(image_n))
    image_list.append(image_n)
    image_props.append(zero_count)

# Find the dictionary with the lowest score
largest_layer = min(image_props, key=lambda x: x["0"])
ans_p1 = largest_layer['1'] * largest_layer['2']
print(f"Part 1: {ans_p1}")

# 0 is black, 1 is white, and 2 is transparent.
# Part 2: Decode the image by layering
def layer_image(old_image, current_image):
    """Combine two layers by overlaying `current_image` onto `old_image`."""
    # Copy the old image to a new list to avoid mutating it directly
    new_image = list(old_image)  
    for pos, pixel in enumerate(old_image):
        if pixel == '2':  # Only replace transparent pixels
            new_image[pos] = current_image[pos]
    return new_image

def decode_message(image_list):
    """Decode the message by layering all images."""
    # Start with the first image as the base layer
    final_image = image_list[0]

    # Overlay each subsequent layer
    for current_image in image_list[1:]:
        final_image = layer_image(final_image, current_image)

    return final_image


def create_image(image, width):
    """Render the image with readable characters."""
    replacements = {'0': ' ', '1': '|', '2': '|'}  # Map pixels to display characters
    # Replace pixel values
    rendered_image = [replacements[pixel] for pixel in image]
    # Print rows of the image
    for i in range(0, len(rendered_image), width):
        print(''.join(rendered_image[i:i + width]))

print("Part 2:")
final_image = decode_message(image_list)
create_image(final_image, size[0])
