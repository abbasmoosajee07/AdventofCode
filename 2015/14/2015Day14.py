# Advent of Code - Day 14, Year 2015
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2015/day/14
# Solution by: [abbasmoosajee07]
# Brief: [Rendeer Race]

import os
import re
import numpy as np
import pandas as pd
D14_file = 'Day14_input.txt'
D14_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D14_file)

with open(D14_file_path) as file:
    reindeer_race = file.read()
    
reindeer_race = reindeer_race.splitlines()

def parse_reindeer_info(instruction):
    match = re.search(r"(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.", instruction)

    if match:
        reindeer = match.group(1)
        speed = int(match.group(2))
        flight_time = int(match.group(3))
        rest_time = int(match.group(4))
        
        # Return in the required format
        return [reindeer, speed, flight_time, rest_time]
    else:
        print(f"Instruction does not match: {instruction}")
        return None


def useful_time(time_n, time_req, max_time):
    time_left = max_time - time_n
    if time_req < time_left: 
        return time_req
    else:
        return time_left


reindeer_props = np.empty((0, 4))
for n in range(len(reindeer_race)):
    reindeer_n = parse_reindeer_info(reindeer_race[n])
    reindeer_props = np.vstack((reindeer_props, reindeer_n))


def reindeer_flight(reindeer_props, max_time, flight_array):
    flight_time = 0
    distance_covered = 0

    fly_duration = int(reindeer_props[2])  # duration it can fly before resting
    rest_duration = int(reindeer_props[3])  # duration it needs to rest

    while flight_time < max_time:
        # Reindeer's flying phase
        dt = useful_time(flight_time, fly_duration, max_time)
        distance_covered += int(reindeer_props[1]) * dt
        flight_array[0,flight_time:flight_time + dt] = int(reindeer_props[1])
        flight_time += dt

        # Reindeer's resting phase
        dt = useful_time(flight_time, rest_duration, max_time)
        flight_array[0,flight_time:flight_time + dt] = 0
        flight_time += dt  # No distance covered during rest
        
    return distance_covered, flight_time, flight_array

max_time = 2503
final_results = []
full_timeline = pd.DataFrame()
for n in range(len(reindeer_props)):
    reindeer_n = reindeer_props[n]
    flight_array = np.full((1, max_time), np.nan)
    
    distance, total_time, flight_timeline = reindeer_flight(reindeer_n, max_time, flight_array)
    final_results.append([str(reindeer_n[0]),distance])
    
    flight_timeline = pd.DataFrame(flight_timeline)
    full_timeline = pd.concat([full_timeline, flight_timeline], ignore_index=True)



# Find the reindeer with the maximum distance
max_reindeer = max(final_results, key=lambda x: x[1])
print(f"The reindeer with the maximum distance is {max_reindeer[0]} with {max_reindeer[1]} km.")


total_flight = full_timeline.cumsum(axis=1)  # axis=1 for row-wise cumulative sum
# print(total_flight)

points_df = pd.DataFrame(0, index=total_flight.index, columns=total_flight.columns)

# Assign points based on the largest value in each column
for column in total_flight.columns:
    max_value = total_flight[column].max()  # Find the maximum value in the column
    # Identify all rows with the maximum value and assign points
    points_df[column] = (total_flight[column] == max_value).astype(int)  # Assign 1 point for max values

# Display the points DataFrame
total_points = points_df.cumsum(axis=1)  # axis=1 for row-wise cumulative sum

final_df = pd.DataFrame(final_results, columns=['Reindeer', 'OG'])
final_df['New'] = total_points.iloc[:, -1]

print(final_df)

