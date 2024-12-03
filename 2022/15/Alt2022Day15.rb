=begin
Advent of Code - Day 15, Year 2022
Solution Started: Dec 3, 2024
Puzzle Link: https://adventofcode.com/2022/day/15
Solution by: abbasmoosajee07
Brief: [Sensors and Beacons Area Coverage]
=end

#!/usr/bin/env ruby

require 'pathname'

# Define file name and extract complete path to the input file
D15_file = "Day15_input.txt"
D15_file_path = Pathname.new(__FILE__).dirname + D15_file

# Read and sort input data into a grid
input_data = File.read(D15_file_path).strip.split("\n")

# Method to parse input data
def parse_input(input_list)
  sensor_beacon = []
  pattern = /Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)/
  input_list.each do |sensor|
    match = pattern.match(sensor)
    sx, sy, bx, by = match.captures.map(&:to_i)
    sensor_beacon << [[sx, sy], [bx, by]]
  end
  sensor_beacon
end

# Method to calculate Manhattan distance
def calc_manhattan_distance(x1, y1, x2, y2)
  (x1 - x2).abs + (y1 - y2).abs
end

# Method to get the x-range for a specific row from a sensor
def get_x_range_for_row(sensor, row)
  sx, sy = sensor[0]
  bx, by = sensor[1]
  dist = calc_manhattan_distance(sx, sy, bx, by)

  # Check if the row is within the sensor's coverage area
  row_distance = (sy - row).abs
  return nil if row_distance > dist

  # Calculate the horizontal range of coverage on this row
  horizontal_range = dist - row_distance
  [sx - horizontal_range, sx + horizontal_range]
end

def count_unique_coverage_on_row(sensor_beacon_pairs, row)
  ranges = []

  # Get the range of coverage for each sensor
  sensor_beacon_pairs.each do |pair|
    range_for_row = get_x_range_for_row(pair, row)
    ranges << range_for_row if range_for_row
  end

  # If no ranges are found, return 0 as there is no coverage
  return 0 if ranges.empty?

  # Sort the ranges by the starting x-coordinate
  ranges.sort!

  # Merge overlapping or adjacent ranges
  merged_ranges = []
  current_range = ranges.first

  ranges[1..].each do |r|
    if r[0] <= current_range[1] + 1
      current_range = [current_range[0], [current_range[1], r[1]].max]
    else
      merged_ranges << current_range
      current_range = r
    end
  end

  # Add the last range
  merged_ranges << current_range

  # Count the total number of covered x-coordinates, excluding beacon positions
  total_coverage = 0
  beacon_positions = sensor_beacon_pairs.map { |_, beacon| beacon }

  merged_ranges.each do |r|
    (r[0]..r[1]).each do |x|
      total_coverage += 1 unless beacon_positions.include?([x, row])
    end
  end

  total_coverage
end

# Method to find a non-covered spot
def find_non_covered_spot(sensor_beacon_pairs, max_row = 4_000_000)
  # Track ranges of covered x-coordinates for each row
  (0..max_row).each do |row|
    ranges = []

    # Get the range of coverage for each sensor
    sensor_beacon_pairs.each do |pair|
      range_for_row = get_x_range_for_row(pair, row)
      ranges << range_for_row if range_for_row
    end

    # Sort the ranges by the starting x-coordinate
    ranges.sort!

    # Merge overlapping or adjacent ranges
    merged_ranges = []
    current_range = ranges.first

    ranges[1..].each do |r|
      if r[0] <= current_range[1] + 1
        current_range = [current_range[0], [current_range[1], r[1]].max]
      else
        merged_ranges << current_range
        current_range = r
      end
    end

    # Add the last range
    merged_ranges << current_range

    # After merging, check for a gap in coverage
    merged_ranges.each do |r|
      # If there's a gap before the start of the range, return that position
      return [r[0] - 1, row] if r[0] > 0
    end
  end

  nil  # If no valid spot is found
end

# Example Row to check
row = 2_000_000
sensor_beacon_pairs = parse_input(input_data)

# Calculate total coverage
ans_p1 = count_unique_coverage_on_row(sensor_beacon_pairs, row)
puts "Part 1: #{ans_p1}"

# Find a non-covered spot
non_covered_spot = find_non_covered_spot(sensor_beacon_pairs)
if non_covered_spot
  part_2 = (non_covered_spot[0] * 4_000_000) + non_covered_spot[1]
  puts "Part 2: #{part_2}"
else
  puts "Part 2: No non-covered spot found"
end

