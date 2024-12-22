=begin
Advent of Code - Day 22, Year 2024
Solution Started: Dec 22, 2024
Puzzle Link: https://adventofcode.com/2024/day/22
Solution by: abbasmoosajee07
Brief: [Optimum Price in random price lists]
=end

#!/usr/bin/env ruby

require 'pathname'

# Define file name and extract complete path to the input file
D22_file = "Day22_input.txt"
D22_file_path = Pathname.new(__FILE__).dirname + D22_file

# Read the input data
input_data = File.readlines(D22_file_path)

# Function to mix two numbers using XOR
def mix_number(value1, value2)
  value1 ^ value2
end

# Function to prune a number by applying modulo
def prune_number(value, modulo = 16777216)
  value & (modulo - 1) # Faster than `%` for powers of 2
end

# Function to evolve the secret number through a series of transformations
def evolve_secret_number(secret_number)
  mixed_1 = mix_number(secret_number, secret_number << 6) # `* 64` becomes `<< 6`
  pruned_1 = prune_number(mixed_1)

  mixed_2 = mix_number(pruned_1, pruned_1 >> 5) # `/ 32` becomes `>> 5`
  pruned_2 = prune_number(mixed_2)

  mixed_3 = mix_number(pruned_2, pruned_2 << 11) # `* 2048` becomes `<< 11`
  prune_number(mixed_3)
end

# Process a single buyer and evolve their secret number over a specified number of generations
def process_buyer(buyer, generations = 2000)
  secret_number = buyer
  price_list = []  # List to store differences in last digits

  generations.times do
    secret_number = evolve_secret_number(secret_number)  # Evolve the number
    last_digit = secret_number % 10  # Get last digit directly without string conversion

    price_list.push(secret_number)
  end
  return price_list, secret_number
end

# Function to simulate all buyers and return the total sum of their final secret numbers
def simulate_all_buyers(buyer_list)
  total_nums = 0
  price_dict = {}

  buyer_list.each do |buyer|
    digit_list, final_number = process_buyer(buyer)
    price_dict[buyer] = digit_list
    total_nums += final_number
  end

  [price_dict, total_nums]
end

# Function to handle banana sales and sequence handling
def sell_bananas(price_dict, seq_len = 4)
  all_sequences = Hash.new(0)

  price_dict.each do |buyer_no, full_price|
    price_list = full_price.map { |x| x % 10 }
    sequence_dict = Hash.new(0)  # Initialize Hash with default value 0 for missing keys

    (seq_len - 1..price_list.length - 1).each do |idx|  # Look for sequences of length `seq_len`
      price_deltas = (1..seq_len).map do |i|
        price_list[idx - (seq_len - i)] - price_list[idx - (seq_len - i + 1)]
      end

      sequence_dict[price_deltas] = price_list[idx] unless sequence_dict.key?(price_deltas)
    end

    # Update the global sequence dictionary with the local sequence counts
    sequence_dict.each do |sequence, price|
      all_sequences[sequence] += price
    end
  end

  return all_sequences
end

# Parse input data
input_nums = input_data.map(&:to_i)

price_dict, ans_p1 = simulate_all_buyers(input_nums)
puts "Part 1: #{ans_p1}"

# Sale sequence handling
sale_dict = sell_bananas(price_dict)

# Find the sequence with the maximum count
if !sale_dict.empty?
  sell_sequence = sale_dict.max_by { |sequence, price| price }
  bananas_sold = sell_sequence[1]
  puts "Part 2: #{bananas_sold}"
end
