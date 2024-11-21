# Advent of Code - Day 17, Year 2015
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2015/day/17
# Solution by: [abbasmoosajee07]
# Brief: [Container and liquid storage Problem]

require 'pathname'

# Define the file path
D17_file = 'Day17_input.txt'
D17_file_path = Pathname.new(__FILE__).dirname + D17_file

# Read the contents of the file
containers = File.readlines(D17_file_path).map(&:chomp)

# Convert strings to integers
containers = containers.map(&:to_i)
eggnog = 150

# Initialize a list to hold valid combinations
valid_combinations = []
combo_length = []
counter = 0

# Generate all combinations of the numbers
(1..containers.length).each do |r|
  containers.combination(r) do |combination|
    if combination.sum == eggnog
      counter += 1
      valid_combinations << combination
      combo_length << combination.length
    end
  end
end

# # Print the valid combinations
# valid_combinations.each do |combo|
#   # puts combo.inspect
# end


min_conts = combo_length.min()
min_combs=  combo_length.count(min_conts) 

puts "Part 1: The number of different combinations is #{counter} \n"

puts "The minimum No containers required #{min_conts}, used in #{min_combs} different combinations \n"