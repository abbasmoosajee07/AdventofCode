"""Advent of Code - Day 22, Year 2024
Solution Started: Dec 22, 2024
Puzzle Link: https://adventofcode.com/2024/day/22
Solution by: abbasmoosajee07
Brief: [Optimum Price in random price lists]
"""

import os
import time
from collections import defaultdict

start_time = time.time()

# Load the input data from the specified file path
D22_file = "Day22_input.txt"
D22_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D22_file)

# Read and sort input data into a grid
with open(D22_file_path) as file:
    input_data = file.read().strip().split('\n')
    input_nums = list(map(int, input_data))

def evolve_secret_number(secret_number: int) -> int:
    """Evolves the secret number through a series of transformations."""
    def mix_number(value1: int, value2: int) -> int:
        """Returns the result of XOR between value1 and value2."""
        return value1 ^ value2

    def prune_number(value: int, modulo: int = 16777216) -> int:
        """Applies modulo operation to 'prune' the value."""
        return value % modulo
    # First transformation step: multiply, mix, and prune
    factor_1 = 64
    mixed_1 = mix_number(secret_number, secret_number * factor_1)
    pruned_1 = prune_number(mixed_1)

    # Second transformation step: divide, mix, and prune
    divisor_2 = 32
    mixed_2 = mix_number(pruned_1, pruned_1 // divisor_2)
    pruned_2 = prune_number(mixed_2)
    
    # Third transformation step: multiply, mix, and prune
    factor_3 = 2048
    mixed_3 = mix_number(pruned_2, pruned_2 * factor_3)
    final_num = prune_number(mixed_3)

    # The final evolved number after all transformations
    return final_num

def process_buyer(buyer: int, generations: int = 2000) -> int:
    """Process a single buyer and evolve their secret number over a specified number of generations."""
    secret_number = buyer
    price_list = []  # List to store differences in last digits

    for gen in range(generations):
        secret_number = evolve_secret_number(secret_number)  # Evolve the number

        price_list.append(secret_number)

    return price_list, secret_number

def simulate_all_buyers(buyer_list: list[int]) -> int:
    """Simulate all buyers, evolve their secret numbers, and return the total sum."""
    total_nums = 0
    price_dict = {}
    for buyer in buyer_list:
        price_list, final_number = process_buyer(buyer)  # Use the new function to process each buyer
        price_dict[buyer] = price_list
        total_nums += final_number
    return price_dict, total_nums

def sell_bananas(price_dict: dict, seq_len: int = 4) -> dict:
    all_sequences = defaultdict(int)

    for buyer_no, full_price in price_dict.items():
        price_list = list(map(lambda x: x % 10, full_price))
        sequence_dict = defaultdict(int)  # Initialize defaultdict with default value 0 for missing keys
        for idx in range(seq_len - 1, len(price_list)):  # Look for sequences of length 4
            price_deltas = tuple(
                price_list[idx - (seq_len - i)] - price_list[idx - (seq_len - i + 1)]
                for i in range(1, seq_len + 1)
            )
            if price_deltas not in sequence_dict:
                sequence_dict[price_deltas] = price_list[idx]

        # Update the global sequence dictionary with the local sequence counts
        for sequence, price in sequence_dict.items():
            all_sequences[sequence] += price

    return all_sequences

# Example Test
price_dict, ans_p1 = simulate_all_buyers(input_nums)
print("Part 1:", ans_p1)

# # Sale sequence handling
sale_dict = sell_bananas(price_dict)

# Find the sequence with the maximum count
if sale_dict:
    sell_sequence = max(sale_dict, key=sale_dict.get)
    bananas_sold = sale_dict[sell_sequence]
    print(f"Part 2: {bananas_sold}")

print("Time:", time.time() - start_time)