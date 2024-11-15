# Advent of Code - Day 16, Year 2016
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2016/day/16
# Solution by: [abbasmoosajee07]
# Brief: [Filling disk space, and calculating checksum]

import sys, os

# Load the input data from the specified file path
D16_file = "Day16_input.txt"
D16_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D16_file)

# Read and sort input data into a grid
with open(D16_file_path) as file:
    input_data = file.read().strip()
    
# increas the maximum num of str stored in variables
sys.set_int_max_str_digits(10000000) 

def look_and_say1(number):
    # Convert the number to a string to work with each digit
    num_str = str(number)
    
    a = num_str       # Callng data "a"
    b = num_str      # Making copy of "a", called "b"
    b = b[::-1]    # Reverse order of characters in b
    b_list = []
    for n in range(len(b)):
        bn = str(abs(1-int(b[n])))
        b_list.append(bn)
    b = "".join(b_list)
    
    final_str = "".join([a,'0',b])
    print(final_str)
    
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

def extend_data(number):
    # Convert the number to a string
    num_str = str(number)
    # Reverse the number
    #  Flip lip each digit (1 -> 0, 0 -> 1)
    reversed_flipped = ''.join(str(1 - int(char)) for char in num_str[::-1])

    # Concatenate original number, '0', and reversed/flipped number
    final_str = num_str + '0' + reversed_flipped

    return final_str

def fill_disk_space(avail_space, num_i):
    str_len = 0
    num = num_i
    
    while str_len < avail_space:
        final_string = extend_data(num)
        str_len = len(final_string)
        num = final_string
        
    if str_len > avail_space:
        final_string = final_string[0:avail_space]
        
    return final_string

def calculate_checksum(data):
    # Keep calculating checksum until its length is odd
    while len(data) % 2 == 0:
        checksum = ""
        # Compare each pair of characters
        for i in range(0, len(data), 2):
            if data[i] == data[i + 1]:
                checksum += '1'  # Same pair (00 or 11) -> '1'
            else:
                checksum += '0'  # Different pair (01 or 10) -> '0'
        data = checksum  # Update data to be the new checksum
    return data  # Return the checksum once its length is odd


""""--------------------- Part 1 ---------------------"""
P1_disk_space = 272
P1_str = fill_disk_space(P1_disk_space, int(input_data))
P1_checksum = calculate_checksum(P1_str)
print(f"The Checksum for string filling disk space of {P1_disk_space}, is {P1_checksum}")

""""--------------------- Part 2 ---------------------"""
P2_disk_space = 35651584
P2_str = fill_disk_space(P2_disk_space, int(input_data))
P2_checksum = calculate_checksum(P2_str)
print(f"The Checksum for string filling disk space of {P2_disk_space}, is {P2_checksum}")