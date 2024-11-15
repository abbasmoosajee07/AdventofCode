# Advent of Code - Day 10, Year 2016
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2016/day/10
# Solution by: [abbasmoosajee07]
# Brief: [Bot Balancing]

import re, collections, os

D10_file = 'Day10_input.txt'
D10_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D10_file)

# Read input file
with open(D10_file_path) as file:
    input_lines = file.read().splitlines()
    
bot = collections.defaultdict(list)
output = collections.defaultdict(list)

# Initialize an empty dictionary to store bot input_lines
pipeline = {}

# Parse the input_lines and populate the bot and pipeline data
for line in input_lines:
    # If the line starts with 'value', it means a value is given to a bot
    if line.startswith('value'):
        # Extract the value (n) and the bot (b) it is assigned to
        n, b = map(int, re.findall(r'-?\d+', line))
        # Append the value n to the list of values for bot b
        bot[b].append(n)

    # If the line starts with 'bot', it contains an instruction for a bot's behavior
    if line.startswith('bot'):
        # Extract the bot number (who) and the numbers of the bots/outputs it will pass to
        who, n1, n2 = map(int, re.findall(r'-?\d+', line))
        # Extract the type (bot or output) for each target (t1 and t2)
        t1, t2 = re.findall(r' (bot|output)', line)
        # Store the instruction for this bot in the pipeline dictionary
        pipeline[who] = (t1, n1), (t2, n2)

# Main loop to process the bots' actions
while bot:
    # Iterate through all bots (using a copy of bot to avoid modification during iteration)
    for k, v in dict(bot).items():
        # Check if the bot has exactly 2 values to process
        if len(v) == 2:
            # Remove the bot from the list (pop) and sort its two values
            v1, v2 = sorted(bot.pop(k))
            # If the values are 17 and 61, print the bot number (this is part of the puzzle's goal)
            if v1 == 17 and v2 == 61: 
                print(f"Part 1: {k}")
            # Retrieve the input_lines for the current bot from the pipeline
            (t1, n1), (t2, n2) = pipeline[k]
            # Pass the smaller value (v1) to the first target (t1)
            eval(t1)[n1].append(v1)
            # Pass the larger value (v2) to the second target (t2)
            eval(t2)[n2].append(v2)

# After the bots are done, calculate the product of the values in output bins 0, 1, and 2
a, b, c = (output[k][0] for k in [0, 1, 2])
# Print the product of these three values (again, part of the puzzle)
print(f"Part 2: {a * b * c}")
