=begin
Advent of Code - Day 1, Year 2023
Solution Started: Dec 17, 2024
Puzzle Link: https://adventofcode.com/2023/day/1
Solution by: abbasmoosajee07
Brief: [Numbers in strings]
=end

#!/usr/bin/env ruby

require 'pathname'

# Define file name and extract complete path to the input file
D01_file = "Day01_input.txt"
D01_file_path = Pathname.new(__FILE__).dirname + D01_file

# Read the input data
input_data = File.readlines(D01_file_path).map(&:strip)

# Initialize first_sum and second_sum to 0
first_sum = 0
second_sum = 0

# Loop through each line in input_data
input_data.each do |line|
  # Initialize arrays to store digits for first_sum and second_sum
  first_digits = []
  second_digits = []

  # Loop through each character in the line
  line.chars.each_with_index do |char, idx|
    if char.match?(/\d/)
      first_digits << char
      second_digits << char
    else
      # Loop through number words to check if they start at the current index
      ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'].each_with_index do |word, index|
        if line[idx..].start_with?(word)
          second_digits << (index + 1).to_s
        end
      end
    end
  end

  # Concatenate the first and last digits for first_sum and second_sum
  first_sum += (first_digits[0] + first_digits[-1]).to_i if first_digits.any?
  second_sum += (second_digits[0] + second_digits[-1]).to_i if second_digits.any?
end

# Print the final first_sum and second_sum values
puts "Part 1: #{first_sum}"
puts "Part 2: #{second_sum}"
