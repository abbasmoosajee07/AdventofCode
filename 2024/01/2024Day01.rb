=begin
Advent of Code - Day 1, Year 2024
Solution Started: Dec 1, 2024
Puzzle Link: https://adventofcode.com/2024/day/1
Solution by: abbasmoosajee07
Brief: [Code/Problem Description]
=end

#!/usr/bin/env ruby

require 'pathname'

# Define file name and extract complete path to the input file
D01_file = "Day01_input.txt"
D01_file_path = Pathname.new(__FILE__).dirname + D01_file

# Read the input data
input_data = File.readlines(D01_file_path).map(&:strip)

split_nums = input_data.map { |row| row.split("  ").map(&:strip) }

# Sort the two columns separately
num_1_list = split_nums.map { |row| row[0] }.sort
num_2_list = split_nums.map { |row| row[1] }.sort

# Transpose the sorted columns into pairs
num_list = num_1_list.zip(num_2_list)

# Calculate the sum of absolute differences
sum = num_list.reduce(0) do |acc, (num_1, num_2)|
  acc + (num_1.to_i - num_2.to_i).abs
end
puts "Part 1: #{sum}"

# Calculate the second sum based on counts of elements in the second list
num_2_count = num_2_list.tally
sum_2 = num_1_list.reduce(0) do |acc, num_1|
  if num_2_count[num_1]
    acc + num_1.to_i * num_2_count[num_1]
  else
    acc
  end
end
puts "Part 2: #{sum_2}"