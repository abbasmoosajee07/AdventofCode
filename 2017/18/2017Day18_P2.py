# Advent of Code - Day 18, Year 2017
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2017/day/18
# Solution by: [abbasmoosajee07]
# Brief: [Computing Registers, P2]

import os, re, copy
import pandas as pd
import numpy as np
from collections import defaultdict

# Load the input data from the specified file path
D18_file = "Day18_input.txt"
D18_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D18_file)

# Load instructions from file
with open(D18_file_path, 'r') as f:
    instr = [line.split() for line in f.read().strip().split("\n")]

# Register dictionaries for each program
d1, d2 = defaultdict(int), defaultdict(int)
d2['p'] = 1
ds = [d1, d2]

# Helper function to get values
def get(s):
    return d[s] if s.isalpha() else int(s)

# Initialize tracking variables
tot = 0
ind = [0, 0]       # Instruction indices for both programs
snd = [[], []]     # Queues of sent data for each program
state = ["ok", "ok"] # "ok" or "r" for waiting or "done" if finished

# Program selection
pr = 0           # Start with program 0
d = ds[pr]       # Set current program's registers
i = ind[pr]      # Set current program's instruction index

while True:
    # Parse each command
    cmd, *args = instr[i]
    
    if cmd == "snd":        # send command
        if pr == 1:         # if program 1 is sending, count it
            tot += 1
        snd[pr].append(get(args[0])) # send value to the program's queue

    elif cmd == "set":      # set command
        d[args[0]] = get(args[1])

    elif cmd == "add":      # add command
        d[args[0]] += get(args[1])

    elif cmd == "mul":      # multiply command
        d[args[0]] *= get(args[1])

    elif cmd == "mod":      # modulo command
        d[args[0]] %= get(args[1])

    elif cmd == "rcv":      # receive command
        if snd[1 - pr]:     # if there's data in the other program's queue
            state[pr] = "ok"
            d[args[0]] = snd[1 - pr].pop(0) # receive value
        else:               # no data to receive
            if state[1 - pr] == "done":
                break       # deadlock: both programs done
            if len(snd[pr]) == 0 and state[1 - pr] == "r":
                break       # deadlock: both programs waiting
            ind[pr] = i     # save current instruction index
            state[pr] = "r" # set program to receiving state
            pr = 1 - pr     # switch programs
            i = ind[pr] - 1 # reset index for new program
            d = ds[pr]      # switch registers

    elif cmd == "jgz":      # jump if greater than zero command
        if get(args[0]) > 0:
            i += get(args[1]) - 1
    
    # Move to the next instruction
    i += 1

    # Check if the current program has exited the instruction range
    if not (0 <= i < len(instr)):
        if state[1 - pr] == "done":
            break           # both programs finished
        state[pr] = "done"  # mark the current program as done
        ind[pr] = i         # save current program index
        pr = 1 - pr         # switch programs
        i = ind[pr]         # reset instruction pointer
        d = ds[pr]          # switch registers

print("Program 1 sent a value", tot, "times.")
