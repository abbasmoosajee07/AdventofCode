=begin
Advent of Code - Day 13, Year 2024
Solution Started: Dec 13, 2024
Puzzle Link: https://adventofcode.com/2024/day/13
Solution by: abbasmoosajee07
Brief: [Solving Simultaneous Equations]
=end

#!/usr/bin/env ruby

require 'pathname'

# Define file name and extract complete path to the input file
D13_file = "Day13_input.txt"
D13_file_path = Pathname.new(__FILE__).dirname + D13_file

# Read the input data
input_data = File.readlines(D13_file_path).map(&:strip)

# Required Libraries
# require 'fileutils'
# require 'csv'
# require 'matrix'


# Read and sort input data into a grid
input_data = File.read(D13_file_path).strip.split("\n\n")

def parse_input(input_list)
  claw_machine = {}
  input_list.each_with_index do |machine, no|
    match = machine.scan(/\d+/).map(&:to_i)
    a_x, a_y, b_x, b_y, prize_x, prize_y = match
    claw_machine[no + 1] = {
      'A_x' => a_x, 'A_y' => a_y,
      'B_x' => b_x, 'B_y' => b_y,
      'Prize_x' => prize_x, 'Prize_y' => prize_y
    }
  end
  claw_machine
end

def solve_equations(prize_x, prize_y, a_x, a_y, b_x, b_y)
  # Calculate the number of times to press button B (press_B)
  numerator_b = prize_y - (prize_x * a_y.to_f / a_x)
  denominator_b = b_y - (b_x * a_y.to_f / a_x)

  if denominator_b == 0  # Prevent division by zero
    return 0, 0, 0
  end

  press_b = numerator_b / denominator_b

  # Calculate the number of times to press button A (press_A)
  press_a = (prize_x - press_b * b_x) / a_x

  # Convert to integers for verification
  int_a = press_a.round
  int_b = press_b.round

  # Verify if the calculated presses match the prize coordinates
  if (int_a * a_x + int_b * b_x == prize_x) && (int_a * a_y + int_b * b_y == prize_y)
    tokens = (3 * int_a) + int_b
    return int_a, int_b, tokens
  end

  return 0, 0, 0
end

def calc_min_tokens(claw_machines, prize_shift = 0)
  total_tokens = 0
  claw_machines.each do |_, test_machine|
    prize_x = test_machine['Prize_x'] + prize_shift
    prize_y = test_machine['Prize_y'] + prize_shift
    a_x = test_machine['A_x']
    a_y = test_machine['A_y']
    b_x = test_machine['B_x']
    b_y = test_machine['B_y']

    press_a, press_b, tokens = solve_equations(prize_x, prize_y, a_x, a_y, b_x, b_y)
    total_tokens += tokens
  end
  total_tokens
end

claw_dict = parse_input(input_data)
ans_p1 = calc_min_tokens(claw_dict)
puts "Part 1: #{ans_p1}"

ans_p2 = calc_min_tokens(claw_dict, 10_000_000_000_000)
puts "Part 2: #{ans_p2}"
