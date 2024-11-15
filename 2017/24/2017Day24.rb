# Advent of Code - Day 24, Year 2017
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2017/day/24
# Solution by: [abbasmoosajee07]
# Brief: [Building Bridges V_Ruby]

require 'pathname'
# Load the input data from the specified file path
D24_file = "Day24_input.txt"

# Define the file path
D24_file_path =  Pathname.new(__FILE__).dirname.join(D24_file)
# Read the input data and parse it into components

components = File.readlines(D24_file_path).map do |line|
  line.chomp.split('/').map(&:to_i)
end

def find_bridges(components, bridge = [], port = 0)
  possible_bridges = [bridge]

  components.each_with_index do |component, index|
    if component.include?(port)
      # Create a new bridge with the current component included
      next_port = component[0] == port ? component[1] : component[0]
      new_components = components.reject.with_index { |_, i| i == index }
      possible_bridges += find_bridges(new_components, bridge + [component], next_port)
    end
  end

  possible_bridges
end

# Generate all possible bridges starting with port 0
all_bridges = find_bridges(components)

# Calculate the strengths of all possible bridges
bridge_strengths = all_bridges.map { |bridge| bridge.flatten.sum }
strongest_bridge_strength = bridge_strengths.max

# Find the longest bridge (if multiple, choose the strongest of them)
longest_bridge = all_bridges.max_by { |bridge| [bridge.size, bridge.flatten.sum] }
longest_bridge_strength = longest_bridge.flatten.sum

# Output all results
puts "Strongest bridge strength: #{strongest_bridge_strength}"
puts "Longest bridge strength: #{longest_bridge_strength}"
