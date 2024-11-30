=begin
Advent of Code - Day 1, Year 2022
Solution Started: Nov 30, 2024
Puzzle Link: https://adventofcode.com/2022/day/1
Solution by: abbasmoosajee07
# Brief: [Cookies and Calories]
=end

#!/usr/bin/env ruby

require 'pathname'

# Define file name and extract complete path to the input file
D01_file = "Day01_input.txt"
D01_file_path = Pathname.new(__FILE__).dirname + D01_file

# Read the input data
input_data = File.readlines(D01_file_path).map(&:strip)

# Split the data into blocks by empty lines
blocks = input_data.join("\n").split("\n\n")

# Parse each block into an array of integers
cookie_list = blocks.map do |block|
  block.split("\n").map(&:to_i)
end

# Part 1: Find the maximum calories
max_calories = cookie_list.map { |list| list.sum }.max
puts "Part 1: #{max_calories}"

# Part 2: Find the sum of the largest three calorie totals
total_calories = cookie_list.map(&:sum)
largest_3 = total_calories.sort.reverse.first(3)
puts "Part 2: #{largest_3.sum}"
