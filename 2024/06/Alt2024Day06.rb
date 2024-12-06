=begin
Advent of Code - Day 6, Year 2024
Solution Started: Dec 6, 2024
Puzzle Link: https://adventofcode.com/2024/day/6
Solution by: abbasmoosajee07
Brief: [Guard Movements]
=end

#!/usr/bin/env ruby

require 'pathname'
require 'set'

# Define file name and extract complete path to the input file
D06_file = "Day06_input.txt"
D06_file_path = Pathname.new(__FILE__).dirname + D06_file

# Read the input data
input_data = File.readlines(D06_file_path).map(&:strip)

# Find all positions of a specific character and return a hash with position as key
def find_positions(input, char = '#', check = true)
  positions = {}
  input.each_with_index do |row, i|
    row.chars.each_with_index do |value, j|
      if check
        positions[[i, j]] = value == char
      else
        positions[[i, j]] = value != char
      end
    end
  end
  positions
end

# Move around the grid avoiding obstacles and tracking visited positions
def move_on_grid(obstacles, start_pos, start_dir, boundary)
  visited = Set.new  # Track visited positions
  rows, cols = boundary

  # Direction mapping: "N" = North, "E" = East, "S" = South, "W" = West
  directions = ["N", "E", "S", "W"]
  direction_deltas = {
    "N" => [-1, 0],
    "E" => [0, 1],
    "S" => [1, 0],
    "W" => [0, -1]
  }

  r, c = start_pos  # Initial position
  current_dir = start_dir  # Initial direction

  loop do
    # Check bounds before moving
    break unless (0 <= r && r < rows && 0 <= c && c < cols)

    # Add the current position to visited
    visited.add([r, c])

    # Calculate the next position
    dr, dc = direction_deltas[current_dir]
    next_r, next_c = r + dr, c + dc

    # If the next position is not an obstacle, move there
    if !obstacles[[next_r, next_c]]
      r, c = next_r, next_c
    else
      # If blocked, turn right
      current_dir = directions[(directions.index(current_dir) + 1) % 4]
    end

    # Debugging output: Show current state
    # puts "Current Position: #{r}, #{c}, Direction: #{current_dir}"
  end

  visited
end

obstacles = find_positions(input_data, '#')
start = find_positions(input_data, '^').key(true)
boundary = [input_data.length, input_data.first.length]
path_p1 = move_on_grid(obstacles, start, 'N', boundary)
puts "Part 1: #{path_p1.length}"

def count_loops(map, pos, dir, seen, recurse)
  directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
  loops = 0
  loop do
    next_pos = directions[dir].zip(pos).map(&:sum)

    case map[next_pos]
    when true
      if recurse
        map[next_pos] = false
        loops += 1 if seen.none? { |p, _| p == next_pos } &&
                      count_loops(map, pos, dir, seen.clone, false)
        map[next_pos] = true
      end
      pos = next_pos
      return true unless seen.add?([pos, dir])
    when false
      dir = (dir + 1) % 4
    when nil
      return recurse && loops
    end
  end
end

map = find_positions(input_data, '#', false)
new_obstacles = count_loops(map, start, 0, Set.new([[start, 0]]), true)
puts "Part 2: #{new_obstacles}"
