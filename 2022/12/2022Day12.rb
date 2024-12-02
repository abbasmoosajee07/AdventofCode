=begin
Advent of Code - Day 12, Year 2022
Solution Started: Dec 1, 2024
Puzzle Link: https://adventofcode.com/2022/day/12
Solution by: abbasmoosajee07
Brief: [Minecraft Grids]
=end

#!/usr/bin/env ruby

require 'pathname'
require 'set'
require 'heap'

# Define file name and extract complete path to the input file
D12_file = "Day12_input.txt"
D12_file_path = Pathname.new(__FILE__).dirname + D12_file

# Read the input
input_lines = File.readlines(D12_file_path).map(&:chomp)

# Convert the input to a 2D array of characters
input_grid = input_lines.map { |line| line.chars }

# Find the positions of 'S' (Start) and 'E' (End)
start_pos = input_grid.each_with_index.flat_map { |row, i| row.each_with_index.select { |x, j| x == "S" }.map { |x, j| [i, j] } }.first
end_pos = input_grid.each_with_index.flat_map { |row, i| row.each_with_index.select { |x, j| x == "E" }.map { |x, j| [i, j] } }.first

# Initialize the number map
number_map = Array.new(input_grid.size) { Array.new(input_grid[0].size, 0) }

# Map letters to numbers (a=1, b=2, ..., z=26)
('a'..'z').each_with_index do |char, i|
  input_grid.each_with_index do |row, r|
    row.each_with_index do |cell, c|
      number_map[r][c] = i + 1 if cell == char
    end
  end
end

# Special cases for 'S' and 'E'
number_map[start_pos[0]][start_pos[1]] = 1  # Start is 1
number_map[end_pos[0]][end_pos[1]] = 26    # End is 26

# Simple priority queue using an array
class SimplePriorityQueue
  def initialize
    @queue = []
  end
  
  def push(priority, item)
    @queue.push([priority, item])
    @queue.sort_by! { |x| x[0] } # Sort by priority (ascending)
  end
  
  def pop
    @queue.shift # Remove and return the item with the highest priority (lowest value)
  end
  
  def empty?
    @queue.empty?
  end
end

# Function to perform Dijkstra's Algorithm forwards
def pathfinder_forwards(start_pos, number_map, end_pos)
  dims = [number_map.size, number_map[0].size]
  distance = Array.new(dims[0]) { Array.new(dims[1], Float::INFINITY) }
  distance[start_pos[0]][start_pos[1]] = 0
  unvisited = Array.new(dims[0]) { Array.new(dims[1], true) }
  
  # Priority queue for Dijkstra's algorithm
  pq = SimplePriorityQueue.new
  pq.push(0, start_pos)

  while !pq.empty?
    dist, current = pq.pop
    
    if current == end_pos
      return dist
    end
    
    next if unvisited[current[0]][current[1]] == false
    
    unvisited[current[0]][current[1]] = false
    current_i, current_j = current

    # Adjacent cells (up, down, left, right)
    adjacent_inds = [
      [current_i, current_j + 1],
      [current_i + 1, current_j],
      [current_i, current_j - 1],
      [current_i - 1, current_j]
    ]

    adjacent_inds.each do |adj|
      adj_i, adj_j = adj
      if adj_i >= 0 && adj_i < dims[0] && adj_j >= 0 && adj_j < dims[1]
        if number_map[adj_i][adj_j] < number_map[current_i][current_j] + 2
          new_dist = dist + 1
          if new_dist < distance[adj_i][adj_j]
            distance[adj_i][adj_j] = new_dist
            pq.push(new_dist, [adj_i, adj_j])
          end
        end
      end
    end
  end
  distance[end_pos[0]][end_pos[1]]
end

# Function to perform Dijkstra's Algorithm backwards
def pathfinder_backwards(end_pos, number_map)
  dims = [number_map.size, number_map[0].size]
  distance = Array.new(dims[0]) { Array.new(dims[1], Float::INFINITY) }
  distance[end_pos[0]][end_pos[1]] = 0
  unvisited = Array.new(dims[0]) { Array.new(dims[1], true) }
  
  # Priority queue for Dijkstra's algorithm
  pq = SimplePriorityQueue.new
  pq.push(0, end_pos)

  while !pq.empty?
    dist, current = pq.pop
    
    if unvisited.flatten.none? { |x| x == true }
      break
    end
    
    next if unvisited[current[0]][current[1]] == false
    
    unvisited[current[0]][current[1]] = false
    current_i, current_j = current

    # Adjacent cells (up, down, left, right)
    adjacent_inds = [
      [current_i, current_j + 1],
      [current_i + 1, current_j],
      [current_i, current_j - 1],
      [current_i - 1, current_j]
    ]

    adjacent_inds.each do |adj|
      adj_i, adj_j = adj
      if adj_i >= 0 && adj_i < dims[0] && adj_j >= 0 && adj_j < dims[1]
        if number_map[adj_i][adj_j] > number_map[current_i][current_j] - 2
          new_dist = dist + 1
          if new_dist < distance[adj_i][adj_j]
            distance[adj_i][adj_j] = new_dist
            pq.push(new_dist, [adj_i, adj_j])
          end
        end
      end
    end
  end
  
  # Find all the lowest points (where number_map == 1)
  lowest_points = []
  number_map.each_with_index do |row, r|
    row.each_with_index do |cell, c|
      lowest_points << [r, c] if cell == 1
    end
  end
  
  # Return the minimum distance to any of the lowest points
  lowest_points.map { |point| distance[point[0]][point[1]] }.min
end

ans_p1 = pathfinder_forwards(start_pos, number_map, end_pos)
ans_p2 = pathfinder_backwards(end_pos, number_map)

# Print the results
puts "Part 1: #{ans_p1}"
puts "Part 2: #{ans_p2}"
