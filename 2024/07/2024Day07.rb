=begin
Advent of Code - Day 7, Year 2024
Solution Started: Dec 9, 2024
Puzzle Link: https://adventofcode.com/2024/day/7
Solution by: abbasmoosajee07
Brief: [Build Numbers]
=end

#!/usr/bin/env ruby

require 'pathname'

# Define file name and extract complete path to the input file
D07_file = "Day07_input.txt"
D07_file_path = Pathname.new(__FILE__).dirname + D07_file

# Read the input data
input_data = File.readlines(D07_file_path).map(&:strip)

# Helper function to check if the combination is valid
def is_valid(target, ns, p2)
  if ns.length == 1
    return ns[0] == target
  end
  
  # Check if the current combination of the first two elements is valid
  if is_valid(target, [ns[0] + ns[1]] + ns[2..-1], p2)
    return true
  end
  
  # Check if the product of the first two elements is valid
  if is_valid(target, [ns[0] * ns[1]] + ns[2..-1], p2)
    return true
  end
  
  # If p2 is true, check if combining the first two elements as a number works
  if p2 && is_valid(target, [Integer(ns[0].to_s + ns[1].to_s)] + ns[2..-1], p2)
    return true
  end
  
  false
end
ans_p1 = 0
ans_p2 = 0
# Iterate through each line in the data
input_data.each do |line|
  target, ns = line.strip.split(":")
  target = target.to_i
  ns = ns.strip.split.map(&:to_i)

  # Check if the target is valid for p1 and p2
  ans_p1 += target if is_valid(target, ns, false)
  ans_p2 += target if is_valid(target, ns, true)
end

# Output results
puts "Part 1: #{ans_p1}"
puts "Part 2: #{ans_p2}"