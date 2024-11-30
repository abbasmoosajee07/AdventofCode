=begin
Advent of Code - Day 9, Year 2022
Solution Started: Nov 30, 2024
Puzzle Link: https://adventofcode.com/2022/day/9
Solution by: abbasmoosajee07
Brief: [Building Ropes]
=end

#!/usr/bin/env ruby

require 'pathname'

# Define file name and extract complete path to the input file
D09_file = "Day09_input.txt"
D09_file_path = Pathname.new(__FILE__).dirname + D09_file

# Read the input data
input_data = File.readlines(D09_file_path).map(&:strip)

def parse_instructions(instructions)
  instruction_list = []
  instructions.each do |command|
    direction, magnitude = command.split(' ')
    instruction_list << [direction, magnitude.to_i]
  end
  instruction_list
end

def build_tail(command_list, start = [0, 0], rope_len = 1)
  # Simulates the movement of a rope's head and tail in a 2D grid.

  # Initialize positions for head and tail
  head_x, head_y = start
  tail_x, tail_y = start

  # Set to track all unique positions visited by the tail
  tail_visited = Set.new
  tail_visited.add([tail_x, tail_y])

  # Movement dictionary: Maps actions to changes in (x, y)
  movement = {
    'U' => [0, 1],   # Move up
    'D' => [0, -1],  # Move down
    'L' => [-1, 0],  # Move left
    'R' => [1, 0]    # Move right
  }

  # Process each command in the command list
  command_list.each do |action, magnitude|
    dx, dy = movement[action]  # Get movement deltas
    magnitude.times do
      # Move the head
      head_x += dx
      head_y += dy

      # Move the tail to stay adjacent to the head
      if (head_x - tail_x).abs > rope_len || (head_y - tail_y).abs > rope_len
        # Move tail closer to head in x-direction
        if head_x != tail_x
          tail_x += (head_x > tail_x ? 1 : -1)
        end
        # Move tail closer to head in y-direction
        if head_y != tail_y
          tail_y += (head_y > tail_y ? 1 : -1)
        end
      end

      # Record the tail's position
      tail_visited.add([tail_x, tail_y])
    end
  end

  # Return the total number of unique positions visited by the tail
  [tail_visited, tail_visited.size]
end

commands = parse_instructions(input_data)
_, ans_p1 = build_tail(commands)
puts "Part 1: #{ans_p1}"

def build_rope(command_list, rope_length = 10, start = [0, 0])
  # Simulates the movement of a rope with multiple knots in a 2D grid.

  # Initialize positions for all knots in the rope
  rope = Array.new(rope_length) { start.dup }

  # Set to track all unique positions visited by the last knot
  tail_visited = Set.new
  tail_visited.add(rope[-1].dup)  # Add initial position of the last knot

  # Movement dictionary: Maps actions to changes in (x, y)
  movement = {
    'U' => [0, 1],   # Move up
    'D' => [0, -1],  # Move down
    'L' => [-1, 0],  # Move left
    'R' => [1, 0]    # Move right
  }

  # Process each command in the command list
  command_list.each do |action, magnitude|
    dx, dy = movement[action]  # Get movement deltas
    magnitude.times do
      # Move the head
      rope[0][0] += dx
      rope[0][1] += dy

      # Propagate movement to the rest of the rope
      (1...rope_length).each do |i|
        head_x, head_y = rope[i - 1]
        tail_x, tail_y = rope[i]

        # Check if the current knot is too far from the knot ahead
        if (head_x - tail_x).abs > 1 || (head_y - tail_y).abs > 1
          # Move the current knot closer to the knot ahead
          if head_x != tail_x
            tail_x += (head_x > tail_x ? 1 : -1)
          end
          if head_y != tail_y
            tail_y += (head_y > tail_y ? 1 : -1)
          end

          # Update the current knot's position
          rope[i] = [tail_x, tail_y]
        end
      end

      # Record the last knot's position
      tail_visited.add(rope[-1].dup)
    end
  end

  # Return the total number of unique positions visited by the last knot
  [tail_visited, tail_visited.size]
end

_, ans_p2 = build_rope(commands)
puts "Part 2: #{ans_p2}"


