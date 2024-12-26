=begin
Advent of Code - Day 9, Year 2023
Solution Started: Dec 26, 2024
Puzzle Link: https://adventofcode.com/2023/day/9
Solution by: abbasmoosajee07
Brief: [Extrapolating Numbers in Sequences]
=end

#!/usr/bin/env ruby

require 'pathname'

# Define file name and extract complete path to the input file
D09_file = "Day09_input.txt"
D09_file_path = Pathname.new(__FILE__).dirname + D09_file

# Read the input data
input_data = File.readlines(D09_file_path).map(&:strip)

# Helper functions to replicate the behavior in Python

def parse_input(input_seq)
  input_seq.map { |row| row.split(' ').map(&:to_i) }
end

def print_triangle(data)
  # Determine the maximum width needed for the numbers
  max_number = data.flatten.max  # Find the largest number
  number_width = max_number.to_s.length  # Determine the width of the largest number
  spacer = ' ' * (number_width + 1)  # Standard space between numbers

  # Create a function to center a number within its gap
  def center(num, number_width)
    num.to_s.center(number_width)
  end

  data.each_with_index do |row, i|
    # For subsequent rows, calculate the alignment
    leading_spaces = spacer * i
    row_content = row.map { |num| center(num, number_width) }.join(spacer)
    puts "#{leading_spaces}#{row_content}"
  end
end

def calculate_diffs(seq)
  # Helper function to calculate differences between consecutive numbers
  seq.each_cons(2).map { |a, b| b - a }
end

def build_number_history(number_sequence)
  full_history = [number_sequence]

  loop do
    # Check if the sequence is all zeros or has only one number
    break if number_sequence.all? { |x| x == 0 } || number_sequence.length == 1

    # Calculate differences and append to history
    diffs = calculate_diffs(number_sequence)
    full_history << diffs

    # Update sequence for the next iteration
    number_sequence = diffs
  end

  full_history
end

def extrapolate_forward(number_history)
  final_value = 0
  use_history = number_history.reverse.dup  # Reverse the history
  updated_history = []

  use_history[0..-2].each_with_index do |seq, seq_no|
    # Calculate new value by adding the last value of the current and next sequence
    new_val = seq[-1] + use_history[seq_no + 1][-1]

    # Update the current sequence and append the new value to the next sequence
    use_history[seq_no + 1] << new_val  # Modify in place

    # Keep track of the updated history
    updated_history << use_history[seq_no + 1]

    # Set final value to the new value
    final_value = new_val
  end

  [updated_history.reverse, final_value]  # Return the updated history and the final value
end

def extrapolate_backwards(number_history)
  final_value = 0
  use_history = number_history.reverse.dup  # Reverse the history and deep copy
  updated_history = []

  # Start with the first sequence (after reversal, it's the last sequence)
  use_history[0].unshift(0)  # Insert 0 at the start of the first sequence
  updated_history << use_history[0]  # Add the modified first sequence to updated history
  
  use_history[1..-1].each_with_index do |seq, seq_no|
    # Calculate new value by subtracting the first value of the current and next sequence
    new_val = seq[0] - use_history[seq_no][0]

    # Insert the new value at the start of the current sequence
    use_history[seq_no + 1].unshift(new_val)

    # Keep track of the updated history
    updated_history << use_history[seq_no + 1]

    # Set final value to the new value
    final_value = new_val
  end

  [updated_history.reverse, final_value]  # Reverse the updated history to restore original order
end

# Test input and the main logic
input_data1 = ['0 3 6 9 12 15', '1 3 6 10 15 21', '10 13 16 21 30 45']
number_seq = parse_input(input_data)

forward_sum, backward_sum = 0, 0
number_seq.each_with_index do |sequence, seq_no|
  num_history = build_number_history(sequence)
  # print_triangle(num_history)
  forward_history, forward_value = extrapolate_forward(num_history)
  forward_sum += forward_value
  back_history, backward_value = extrapolate_backwards(num_history)
  backward_sum += backward_value

  # Uncomment to debug the result by printing the triangles
  # print_triangle(forward_history)
  # print_triangle(back_history)
end

puts "Part 1: #{forward_sum}"
puts "Part 2: #{backward_sum}"
