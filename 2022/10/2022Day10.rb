=begin
Advent of Code - Day 10, Year 2022
Solution Started: Nov 30, 2024
Puzzle Link: https://adventofcode.com/2022/day/10
Solution by: abbasmoosajee07
Brief: [Console computer]
=end

#!/usr/bin/env ruby

require 'pathname'

# Define file name and extract complete path to the input file
D10_file = "Day10_input.txt"
D10_file_path = Pathname.new(__FILE__).dirname + D10_file

# Read the input data
input_data = File.readlines(D10_file_path).map(&:strip)

def run_program(instructions, registers)
  cycle = 0
  signal_strength = {}
  instructions.each do |command|
    command_parts = command.split(' ')
    if command_parts[0] == 'noop'
      cycle += 1
      signal_strength[cycle] = registers[:x]
    elsif command_parts[0] == 'addx'
      cycle += 1
      signal_strength[cycle] = registers[:x]
      cycle += 1
      signal_strength[cycle] = registers[:x]
      registers[:x] += command_parts[1].to_i
    end
  end
  signal_strength
end

signal_strength = run_program(input_data, { x: 1 })

# List of indices to compute the strength
indices = [20, 60, 100, 140, 180, 220]

# Efficient computation using a loop and sum
ans_p1 = indices.sum { |index| index * signal_strength[index] }

puts "Part 1: #{ans_p1}"

def create_picture(signal_dict, size = [6, 40])
  rows, cols = size
  crt_screen = []

  # Iterate over each pixel (cycle)
  (0...(rows * cols)).each do |cycle|
    row = cycle / cols
    col = cycle % cols

    # Get the sprite's center position for the current cycle
    sprite_center = signal_dict[cycle + 1] || 0  # Add 1 to cycle for correct alignment

    # Determine if the pixel should be lit or not (sprite can be at p-1, p, or p+1)
    if [sprite_center - 1, sprite_center, sprite_center + 1].include?(col)
      crt_screen << '|'
    else
      crt_screen << ' '
    end
  end

  # Reshape the screen into rows and columns
  crt_screen.each_slice(cols).to_a
end

message = create_picture(signal_strength)

puts "Part 2:________________________________"
message.each do |row|
  puts row.join
end
