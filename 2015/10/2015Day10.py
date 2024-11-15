# Advent of Code - Day 10, Year 2015
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2015/day/10
# Solution by: [abbasmoosajee07]
# Brief: [Encoding over multiple iterations]

import sys, os

# increas the maximum num of str stored in variables
sys.set_int_max_str_digits(10000000) 

def look_and_say(number):
    # Convert the number to a string to work with each digit
    num_str = str(number)
    
    result = []
    i = 0
    
    while i < len(num_str):
        count = 1  # Start counting occurrences of the current digit
        # Count consecutive identical digits
        while i + 1 < len(num_str) and num_str[i] == num_str[i + 1]:
            count += 1
            i += 1
        
        # Append the count followed by the digit itself
        result.append(f"{count}{num_str[i]}")
        i += 1
    
    # Join the result list into a final string and return as an integer
    return int("".join(result))

# Example usage

D10_file = 'Day10_input.txt'
D10_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D10_file)

with open(D10_file_path) as file:
   input_data = file.read()
   
num = int(input_data)
encoding_runs = 50
encoded_vals = []

for n in range(encoding_runs):
    output = look_and_say(num)
    num = output
    encoded_vals.append(len(str(num)))


print(f"Length of encoded string after 40 runs: {encoded_vals[39]}")
print(f"Length of encoded string after 50 runs: {encoded_vals[49]}")
