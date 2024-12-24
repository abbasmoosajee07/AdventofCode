=begin
Advent of Code - Day 24, Year 2024
Solution Started: Dec 24, 2024
Puzzle Link: https://adventofcode.com/2024/day/24
Solution by: abbasmoosajee07
Brief: [Fixing Circuits]
=end

#!/usr/bin/env ruby

require 'pathname'

# Define file name and extract complete path to the input file
D24_file = "Day24_input.txt"
D24_file_path = Pathname.new(__FILE__).dirname + D24_file

# Read the input data
input_data = File.readlines(D24_file_path).map(&:strip)

def read_input_file(file_path)
  # Reads the input file and returns a list of lines as strings
  File.readlines(file_path).map(&:strip)
end

def find_gate(x_wire, y_wire, gate_type, configurations)
  # Searches for a gate in the configurations based on the given wire names and gate type
  sub_str_a = "#{x_wire} #{gate_type} #{y_wire} -> "
  sub_str_b = "#{y_wire} #{gate_type} #{x_wire} -> "

  configurations.each do |config|
    if config.include?(sub_str_a) || config.include?(sub_str_b)
      return config.split(' -> ').last
    end
  end
  nil
end

def swap_output_wires(wire_a, wire_b, configurations)
  # Swaps the output wires in the configurations for the given wire names
  new_configurations = []

  configurations.each do |config|
    input_wires, output_wire = config.split(' -> ')

    if output_wire == wire_a
      new_configurations << "#{input_wires} -> #{wire_b}"
    elsif output_wire == wire_b
      new_configurations << "#{input_wires} -> #{wire_a}"
    else
      new_configurations << config
    end
  end
  new_configurations
end

def check_parallel_adders(configurations)
  # Checks for parallel adders in the configurations and returns the wires that need to be swapped
  current_carry_wire = nil
  swaps = []
  bit = 0

  loop do
    x_wire = "x#{bit.to_s.rjust(2, '0')}"
    y_wire = "y#{bit.to_s.rjust(2, '0')}"
    z_wire = "z#{bit.to_s.rjust(2, '0')}"

    if bit == 0
      # For the first bit, the current carry wire is the AND gate of x0 and y0
      current_carry_wire = find_gate(x_wire, y_wire, 'AND', configurations)
    else
      # For subsequent bits, find XOR and AND gates and process the carry wires
      ab_xor_gate = find_gate(x_wire, y_wire, 'XOR', configurations)
      ab_and_gate = find_gate(x_wire, y_wire, 'AND', configurations)

      cin_ab_xor_gate = find_gate(ab_xor_gate, current_carry_wire, 'XOR', configurations)
      if cin_ab_xor_gate.nil?
        # If no XOR gate, swap the XOR and AND gates and reset the bit count
        swaps.push(ab_xor_gate, ab_and_gate)
        configurations = swap_output_wires(ab_xor_gate, ab_and_gate, configurations)
        bit = 0
        next
      end

      if cin_ab_xor_gate != z_wire
        # If the XOR gate output is not correct, swap XOR gate and z_wire
        swaps.push(cin_ab_xor_gate, z_wire)
        configurations = swap_output_wires(cin_ab_xor_gate, z_wire, configurations)
        bit = 0
        next
      end

      cin_ab_and_gate = find_gate(ab_xor_gate, current_carry_wire, 'AND', configurations)

      carry_wire = find_gate(ab_and_gate, cin_ab_and_gate, 'OR', configurations)
      current_carry_wire = carry_wire
    end

    bit += 1
    break if bit >= 45
  end

  swaps
end

def find_all_swaps(lines)
  # Main function to solve the problem based on parsed input lines
  divider = lines.index('')
  configurations = lines[(divider + 1)..-1]

  # Check parallel adders and get the necessary swaps
  swaps = check_parallel_adders(configurations)

  # Print the result for part 2 (sorted list of swaps)
  puts "Part 2: #{swaps.sort.join(',')}"
end

find_all_swaps(input_data)
