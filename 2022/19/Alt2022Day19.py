"""Advent of Code - Day 19, Year 2022
Solution Started: Dec 8, 2024
Puzzle Link: https://adventofcode.com/2022/day/19
Solution by: abbasmoosajee07
Brief: [Mining Robots]
"""

#!/usr/bin/env python3

import os, re, copy, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import deque

start_time = time.time()
# Load the input data from the specified file path
D19_file = "Day19_input.txt"
D19_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D19_file)

# Read and sort input data into a grid
with open(D19_file_path) as file:
    input_data = file.read().strip().split('\n')

def parse_input(input_list):
    blueprint_dict = {}
    pattern = r'Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.'
    for line in input_list:
        match = re.findall(pattern, line)[0]
        # print(match)
        blueprint = int(match[0])
        ore_robot = {'ore':int(match[1]), 'clay': 0, 'obsidian': 0}
        clay_robot = {'ore':int(match[2]), 'clay': 0, 'obsidian': 0}
        obsidian_robot = {'ore':int(match[3]), 'clay': int(match[4]), 'obsidian': 0}
        geode_robot = {'ore':int(match[5]), 'clay': 0, 'obsidian': int(match[6])}
        robots = {'ore_robot': ore_robot, 'clay_robot': clay_robot,
                    'obsidian_robot': obsidian_robot, 'geode_robot': geode_robot
                    }
        blueprint_dict[blueprint] = robots
    return blueprint_dict

def solve(Co, Cc, Co1, Co2, Cg1, Cg2, T):
    best = 0
    # state is (ore, clay, obsidian, geodes, r1, r2, r3, r4, time)
    S = (0, 0, 0, 0, 1, 0, 0, 0, T)
    Q = deque([S])
    SEEN = set()
    while Q:
        state = Q.popleft()
        #print(state)
        o,c,ob,g,r1,r2,r3,r4,t = state

        best = max(best, g)
        if t==0:
            continue

        Core = max([Co, Cc, Co1, Cg1])
        if r1>=Core:
            r1 = Core
        if r2>=Co2:
            r2 = Co2
        if r3>=Cg2:
            r3 = Cg2
        if o >= t*Core-r1*(t-1):
            o = t*Core-r1*(t-1)
        if c>=t*Co2-r2*(t-1):
            c = t*Co2 - r2*(t-1)
        if ob>=t*Cg2-r3*(t-1):
            ob = t*Cg2-r3*(t-1)

        state = (o,c,ob,g,r1,r2,r3,r4,t)

        if state in SEEN:
            continue
        SEEN.add(state)

        if len(SEEN) % 1000000 == 0:
            print(t,best,len(SEEN))
        assert o>=0 and c>=0 and ob>=0 and g>=0, state
        Q.append((o+r1,c+r2,ob+r3,g+r4,r1,r2,r3,r4,t-1))
        if o>=Co: # buy ore
            Q.append((o-Co+r1, c+r2, ob+r3, g+r4, r1+1,r2,r3,r4,t-1))
        if o>=Cc:
            Q.append((o-Cc+r1, c+r2, ob+r3, g+r4, r1,r2+1,r3,r4,t-1))
        if o>=Co1 and c>=Co2:
            Q.append((o-Co1+r1, c-Co2+r2, ob+r3, g+r4, r1,r2,r3+1,r4,t-1))
        if o>=Cg1 and ob>=Cg2:
            Q.append((o-Cg1+r1, c+r2, ob-Cg2+r3, g+r4, r1,r2,r3,r4+1,t-1))
    return best

p1 = 0
p2 = 1

blueprints = parse_input(input_data)
for no in blueprints.keys():
    test_blueprint = blueprints[no]
    ore_cost = test_blueprint['ore_robot']['ore']
    clay_cost = test_blueprint['clay_robot']['ore']
    obsidian_cost_ore = test_blueprint['obsidian_robot']['ore']
    obsidian_cost_clay = test_blueprint['obsidian_robot']['clay']
    geode_cost_ore = test_blueprint['geode_robot']['ore']
    geode_cost_obsidian = test_blueprint['geode_robot']['obsidian']

    s1 = solve(ore_cost, clay_cost, obsidian_cost_ore, obsidian_cost_clay, geode_cost_ore, geode_cost_obsidian,24)
    p1 += no*s1
    if no <= 3:
        s2 = solve(ore_cost, clay_cost, obsidian_cost_ore, obsidian_cost_clay, geode_cost_ore, geode_cost_obsidian,32)
        p2 *= s2
print("Part 1:",p1)
print("Part 2:",p2)
print("Total Time:",time.time()-start_time)