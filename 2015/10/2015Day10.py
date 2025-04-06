# Advent of Code - Day 10, Year 2015
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2015/day/10
# Solution by: [abbasmoosajee07]
# Brief: [Encoding over multiple iterations]

import sys, os, time
start_time = time.time()

D10_file = 'Day10_input.txt'
D10_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D10_file)

with open(D10_file_path) as file:
    input_data = file.read()

# increas the maximum num of str stored in variables
sys.set_int_max_str_digits(10000000)

def look_and_say(num_str):
    result = []
    i = 0
    while i < len(num_str):
        count = 1
        while i + 1 < len(num_str) and num_str[i] == num_str[i + 1]:
            count += 1
            i += 1
        result.append(f"{count}{num_str[i]}")
        i += 1
    return ''.join(result)

num = input_data
encoding_runs = 50
encoded_vals = {}

for n in range(encoding_runs):
    num = look_and_say(num)
    encoded_vals[n] = len(num)


print(f"Length of encoded string after 40 runs: {encoded_vals[39]}")
print(f"Length of encoded string after 50 runs: {encoded_vals[49]}")

print(f"Execution Time = {time.time() - start_time:.5f}s")
