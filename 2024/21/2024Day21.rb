# Advent of Code - Day 21, Year 2024
# Solution Started: Dec 21, 2024
# Puzzle Link: https://adventofcode.com/2024/day/21
# Solution by: abbasmoosajee07
# Brief: [Using robots for keypads]

require 'set'

# Load the input data from the specified file path
D21_FILE = "Day21_input.txt"
D21_FILE_PATH = File.join(File.dirname(__FILE__), D21_FILE)

# Read and sort input data into a grid
input_data = File.read(D21_FILE_PATH).strip.split("\n")

def sanitize_paths(paths, start_pos, is_numeric)
  excluded_position = is_numeric ? NUMERIC_POS['X'] : DIRECTIONAL_POS['X']
  sanitized_paths = []

  paths.each do |path|
    current_pos = start_pos.dup
    valid_path = true

    path.each_char do |direction|
      dr, dc = DIRECTIONAL_KEYS[direction]
      current_pos[0] += dr
      current_pos[1] += dc

      if current_pos == excluded_position
        valid_path = false
        break
      end
    end

    sanitized_paths << path if valid_path
  end

  sanitized_paths
end

def get_shortest_paths(start_pos, end_pos, is_numeric)
  vertical_move = end_pos[0] < start_pos[0] ? '^' : 'v'
  vertical_distance = (end_pos[0] - start_pos[0]).abs
  horizontal_move = end_pos[1] < start_pos[1] ? '<' : '>'
  horizontal_distance = (end_pos[1] - start_pos[1]).abs

  raw_paths = [
    vertical_move * vertical_distance + horizontal_move * horizontal_distance,
    horizontal_move * horizontal_distance + vertical_move * vertical_distance
  ]

  sanitize_paths(raw_paths.uniq, start_pos, is_numeric)
end

def solve_numeric_keypad(number_sequence)
  current_pos = NUMERIC_POS['A']
  sequence = []

  number_sequence.each_char do |digit|
    target_pos = NUMERIC_POS[digit]
    paths = get_shortest_paths(current_pos, target_pos, true)
    current_pos = target_pos
    sequence << paths
  end

  sequence.map do |part|
    part.map { |path| path + 'A' }
  end
end

def solve_directional_keypad(direction_sequence)
  current_pos = DIRECTIONAL_POS['A']
  sequence = []

  direction_sequence.each_char do |direction|
    target_pos = DIRECTIONAL_POS[direction]
    paths = get_shortest_paths(current_pos, target_pos, false)
    current_pos = target_pos
    sequence << paths
  end

  sequence.map do |part|
    part.map { |path| path + 'A' }
  end
end

def calculate_min_cost(sequence, depth)
  return sequence.length if depth.zero?

  @memory ||= {}
  return @memory[[sequence, depth]] if @memory.key?([sequence, depth])

  sub_sequences = solve_directional_keypad(sequence)
  cost = sub_sequences.sum do |part|
    part.map { |sub_seq| calculate_min_cost(sub_seq, depth - 1) }.min
  end

  @memory[[sequence, depth]] = cost
  cost
end

def calculate_complexity(keycodes, depth)
  total_cost = 0

  keycodes.each do |key|
    numeric_sequence = solve_numeric_keypad(key)
    level_cost = numeric_sequence.sum do |part|
      part.map { |sequence| calculate_min_cost(sequence, depth) }.min
    end

    total_cost += key[0..-2].to_i * level_cost
  end

  total_cost
end

def parse_keypads(keypad)
  positions = {}

  keypad.each_with_index do |row, r|
    row.each_with_index do |key, c|
      positions[key] = [r, c]
    end
  end

  positions
end

# Global variables
DIRECTIONAL_KEYS = {
  '^' => [-1, 0],
  'v' => [1, 0],
  '>' => [0, 1],
  '<' => [0, -1]
}.freeze

NUMERICAL_KEYPAD = [
  %w[7 8 9],
  %w[4 5 6],
  %w[1 2 3],
  %w[X 0 A]
].freeze

DIRECTION_KEYPAD = [
  %w[X ^ A],
  %w[< v >]
].freeze

NUMERIC_POS = parse_keypads(NUMERICAL_KEYPAD)
DIRECTIONAL_POS = parse_keypads(DIRECTION_KEYPAD)

complex_cost_p1 = calculate_complexity(input_data, 2)
puts "Part 1: #{complex_cost_p1}"

complex_cost_p2 = calculate_complexity(input_data, 25)
puts "Part 2: #{complex_cost_p2}"
