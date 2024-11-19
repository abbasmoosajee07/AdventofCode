# Advent of Code - Day 10, Year 2019
# Solution Started: Nov 18, 2024
# Puzzle Link: https://adventofcode.com/2019/day/10
# Solution by: [abbasmoosajee07]
# Brief: [Monitoring asteroids]

#!/usr/bin/env python3

import os, re, copy, math
import numpy as np
from math import gcd

# Load the input data from the specified file path
D10_file = "Day10_input.txt"
D10_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D10_file)

# Read and sort input data into a grid
with open(D10_file_path) as file:
    input_data = file.read().strip().split('\n')
    asteroid_list = [list(row) for row in input_data]
    asteroid_map = np.array(asteroid_list)

def count_visible_asteroids(asteroid, asteroids):
    visible_asteroids = set()
    x1, y1 = asteroid

    for x2, y2 in asteroids:
        if (x2, y2) == (x1, y1):
            continue

        dx = x2 - x1
        dy = y2 - y1
        divisor = gcd(dx, dy)
        direction = (dx // divisor, dy // divisor)
        visible_asteroids.add(direction)

    return visible_asteroids


def perfect_monitoring_station(asteroid_map):
    max_count = 0
    asteroid_pos = [(x, y) for y, row in enumerate(asteroid_map) for x, value in enumerate(row) if value == '#']
    for idx, pos in enumerate(asteroid_pos):
            visible_asteroids = count_visible_asteroids(pos, asteroid_pos)
            pos_count = len(visible_asteroids)
            # print(pos_count, pos)
            if pos_count > max_count:
                max_count = max(max_count, pos_count)
                ideal_pos = pos
    return max_count, ideal_pos

ans_p1, monitoring_station = perfect_monitoring_station(asteroid_map)
print(f"Part 1: {ans_p1}")

def get_vaporization_order(asteroid_map, station, destroyed_no):
    mx, my = station[0], station[1]
    asteroid_positions = [(x, y) for y, row in enumerate(asteroid_map) for x, value in enumerate(row) if value == '#']

    vaporized_asteroids = [(mx, my)]
    while len(vaporized_asteroids) != len(asteroid_positions):
        closest_asteroids = {}
        for x, y in asteroid_positions:
            if (x, y) not in vaporized_asteroids:
                dx, dy = x - mx, y - my
                dx, dy = dx // math.gcd(dx, dy), dy // math.gcd(dx, dy)
                closest_x, closest_y = closest_asteroids.get((dx, dy), (float('inf'), float('inf')))
                if abs(x - mx) + abs(y - my) < abs(closest_x - mx) + abs(closest_y - my):
                    closest_asteroids[(dx, dy)] = (x, y)
        vaporized_asteroids += sorted(closest_asteroids.values(), key=lambda p: -math.atan2(p[0] - mx, p[1] - my))

    # Assuming `destroyed_no` is the index of the asteroid to retrieve
    score = vaporized_asteroids[destroyed_no][0] * 100 + vaporized_asteroids[destroyed_no][1]

    return score, vaporized_asteroids

ans_p2, _ = get_vaporization_order(asteroid_map, monitoring_station, 200)
print(f'Part 2: {ans_p2}')

