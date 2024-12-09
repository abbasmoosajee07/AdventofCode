=begin
Advent of Code - Day 16, Year 2022
Solution Started: Dec 9, 2024
Puzzle Link: https://adventofcode.com/2022/day/16
Solution by: abbasmoosajee07
Brief: [Pipe Flow]
=end

#!/usr/bin/env ruby

require 'pathname'

# Define file name and extract complete path to the input file
D16_file = "Day16_input.txt"
D16_file_path = Pathname.new(__FILE__).dirname + D16_file

# Read the input data
input_data = File.readlines(D16_file_path).map(&:strip)

def read_puzzle(file)
  File.readlines(file).map do |line|
    line[1..-1].scan(/[A-Z]+|\d+/)
  end
end

graph = {}
flows = {}
indicies = {}
distances = {}
puzzle = read_puzzle(D16_file_path)

# Parse the puzzle data
puzzle.each_with_index do |(valve, flow, *leads), i|
  graph[valve] = leads
  flows[valve] = flow.to_i if flow != '0'
  indicies[valve] = 1 << i
end

# Initialize distances (Floyd-Warshall step 1)
graph.each do |v1, leads|
  leads.each do |v2|
    distances[[v1, v2]] = 1
  end
  graph.each do |v2, _|
    distances[[v1, v2]] ||= 1000
  end
end

# Floyd-Warshall algorithm for shortest path
graph.keys.permutation(3).each do |k, i, j|
  distances[[i, j]] = [distances[[i, j]], distances[[i, k]] + distances[[k, j]]].min
end

# Recursively visit valves to maximize pressure
def visit(valve, minutes, bitmask, pressure, answer, flows, indicies, distances)
  answer[bitmask] = [answer[bitmask] || 0, pressure].max
  flows.each do |valve2, flow|
    remaining_minutes = minutes - distances[[valve, valve2]] - 1
    next if indicies[valve2] & bitmask != 0 || remaining_minutes <= 0
    visit(valve2, remaining_minutes, bitmask | indicies[valve2], pressure + flow * remaining_minutes, answer, flows, indicies, distances)
  end
  answer
end

# Part 1: Max pressure after 30 minutes
part1 = visit('AA', 30, 0, 0, {}, flows, indicies, distances).values.max

# Part 2: Max pressure considering two independent sets of valves
visited2 = visit('AA', 26, 0, 0, {}, flows, indicies, distances)
part2 = visited2.keys.combination(2).map do |bitmask1, bitmask2|
  next if bitmask1 & bitmask2 != 0
  visited2[bitmask1] + visited2[bitmask2]
end.compact.max

puts "Part 1: #{part1}"
puts "Part 2: #{part2}"
