# Advent of Code - Day 2, Year 2015
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2015/day/2
# Solution by: [abbasmoosajee07]
# Brief: [Simple Mulitplation using Strings]

import os 
import array
import numpy as np

D2_file = 'Day02_input.txt'
D2_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D2_file)

with open(D2_file_path) as file:
    wrapping_paper = file.read()

wrapping_paper = wrapping_paper.split()
total_gifts = len(wrapping_paper)

gift_dims = []

for n in range(total_gifts):
    gift_n = wrapping_paper[n]
    ind_n = gift_n.split('x')
    dims_n = [int(num) for num in ind_n]
    dims_array = np.array(dims_n)
    gift_dims.append(dims_array)
gift_dims = np.array(gift_dims)

gift_area = []
ribbon_req = []
for gn in range(total_gifts):
    gift_gn = gift_dims[gn]
    
    # Assign l,w,h dimensions individually
    l = gift_gn[0]
    w = gift_gn[1]
    h = gift_gn[2]
    
    # Calculate all surface areas
    a1 = l * w
    a2 = w * h
    a3 = h * l
    vol = l * w * h
    
    # Determine smallest surface area
    min_a = min([a1,a2,a3])
    
    gift_area_n = (2*a1) + (2*a2) + (2*a3) + min_a
    min_peri = sorted(gift_gn)[:2]
    ribbon_req_n = vol + sum(min_peri)*2
    
    gift_area.append(gift_area_n)
    ribbon_req.append(ribbon_req_n)


print(f"Total Wrapping paper required by elves in sq ft: {sum(gift_area)}.")
print(f"Total Ribbon required by elves in ft: {sum(ribbon_req)}.")
