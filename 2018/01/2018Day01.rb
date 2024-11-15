# Advent of Code - Day 1, Year 2018
# Solved in 201
# Puzzle Link: https://adventofcode.com/2018/day/1
# Solution by: [abbasmoosajee07]
# Brief: [Reading instructions]

require 'pathname'
# Load the input data from the specified file path
D1_file = "Day01_input.txt"
# Define the file path
D1_file_path = Pathname.new(__FILE__).dirname + D1_file

# Read the input data
input_data = File.readlines(D1_file_path).map(&:strip)

# # Print the input data
# puts input_data.inspect

def calc_frequency(strings)
  frequency = 0
  freq_list = []

  strings.each do |str|
    num = str.to_i
    frequency += num
    freq_list << frequency
  end

  return frequency, freq_list
end

freq_P1, _ = calc_frequency(input_data)
puts "Part 1: Cumulative Frequency is #{freq_P1}"

# Initialize variables for part 2
flag = false
frequency = 0
pos = -1
freq_list = []
iter = 0

# Loop until a frequency is found twice
until flag
  pos = (pos + 1) % input_data.length
  num = input_data[pos].to_i
  frequency += num
  iter += 1

  # Print iteration details
  # puts "#{iter} #{pos} #{frequency}"

  if freq_list.include?(frequency)
    flag = true
  else
    freq_list << frequency
  end
end

puts "Part 2: First Double Frequency #{frequency}"
