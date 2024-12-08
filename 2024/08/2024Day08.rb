=begin
Advent of Code - Day 8, Year 2024
Solution Started: Dec 8, 2024
Puzzle Link: https://adventofcode.com/2024/day/8
Solution by: abbasmoosajee07
Brief: [Code/Problem Description]
=end

#!/usr/bin/env ruby

require 'pathname'
require 'set'

# Define file name and extract complete path to the input file
D08_file = "Day08_input.txt"
D08_file_path = Pathname.new(__FILE__).dirname + D08_file

# Read and sort input data into a grid
input_data = File.read(D08_file_path).strip.split("\n")
antenna_map = input_data.map(&:chars)

# Helper method to find antennas in the map
def find_antennas(map)
  antenna_list = Hash.new { |hash, key| hash[key] = [] }
  rows = map.size
  cols = map[0].size

  (0...rows).each do |r|
    (0...cols).each do |c|
      pos = [r, c]
      if map[r][c] != '.'
        antenna_list[map[r][c]] << pos
      end
    end
  end
  antenna_list
end

rows = antenna_map.size
cols = antenna_map[0].size

antenna_list = find_antennas(antenna_map)

antinodes_p1 = Set.new
antinodes_p2 = Set.new

(0...rows).each do |r|
  (0...cols).each do |c|
    antenna_list.each do |freq, coordinate_list|
      coordinate_list.combination(2).each do |(r1, c1), (r2, c2)|
        abs_d1 = (r - r1).abs + (c - c1).abs
        abs_d2 = (r - r2).abs + (c - c2).abs

        dr1 = r - r1
        dr2 = r - r2
        dc1 = c - c1
        dc2 = c - c2

        if r.between?(0, rows - 1) && c.between?(0, cols - 1) && (dr1 * dc2 == dc1 * dr2)
          antinodes_p2.add([r, c])
          if abs_d1 == 2 * abs_d2 || abs_d1 * 2 == abs_d2
            antinodes_p1.add([r, c])
          end
        end
      end
    end
  end
end

puts "Part 1: #{antinodes_p1.size}"
puts "Part 2: #{antinodes_p2.size}"
