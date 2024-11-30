=begin
Advent of Code - Day 8, Year 2022
Solution Started: Nov 30, 2024
Puzzle Link: https://adventofcode.com/2022/day/8
Solution by: abbasmoosajee07
Brief: [Tree Visibility]
=end

#!/usr/bin/env ruby

require 'pathname'

# Define file name and extract complete path to the input file
D08_file = "Day08_input.txt"
D08_file_path = Pathname.new(__FILE__).dirname + D08_file

# Read the input data
input_data = File.readlines(D08_file_path).map(&:strip)
tree_grid = input_data.map { |row| row.chars.map(&:to_i) }

def visibility_from_edge(pos, grid)
  # Define directions: (row_offset, col_offset)
  directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]
  visible_count = 0
  row, col = pos
  num_rows = grid.length
  num_cols = grid[0].length

  directions.each do |dr, dc|
    new_row, new_col = row + dr, col + dc
    current_tree = grid[row][col]
    if new_row.between?(0, num_rows - 1) && new_col.between?(0, num_cols - 1)
      if dr == -1  # upwards
        adjacent_trees = grid[0..new_row].map { |r| r[new_col] }
      elsif dr == 1  # downwards
        adjacent_trees = grid[new_row..].map { |r| r[new_col] }
      elsif dc == 1  # towards right
        adjacent_trees = grid[new_row][new_col..]
      elsif dc == -1  # towards left
        adjacent_trees = grid[new_row][0..new_col]
      end
      tree_set = adjacent_trees.to_set
      visible_count += 1 if tree_set.all? { |tree| current_tree > tree }
    end
  end

  visible_count
end

all_visible_trees = 0

(1..tree_grid.length - 2).each do |x|
  (1..tree_grid[0].length - 2).each do |y|
    visibility = visibility_from_edge([x, y], tree_grid)
    all_visible_trees += 1 if visibility >= 1
  end
end

# Add the trees on the edges
all_visible_trees += (4 * tree_grid.length) - 4
puts "Part 1: #{all_visible_trees}"

def visibility_from_tree(pos, grid)
  directions = [[-1, 0], [1, 0], [0, -1], [0, 1]]  # Up, Down, Left, Right
  row, col = pos
  current_tree = grid[row][col]
  num_rows = grid.length
  num_cols = grid[0].length

  tree_score = []  # Stores visibility distances in all directions

  directions.each do |dr, dc|
    visible_count = 0
    new_row, new_col = row + dr, col + dc

    # Traverse in the current direction until out of bounds or blocked
    while new_row.between?(0, num_rows - 1) && new_col.between?(0, num_cols - 1)
      visible_count += 1  # Count this tree
      if grid[new_row][new_col] >= current_tree
        break  # Stop if a taller or equal tree blocks the view
      end
      new_row += dr
      new_col += dc
    end

    tree_score << visible_count
  end

  # Return the product of visibility distances in all directions
  tree_score.reduce(:*)
end

scenic_score = 0

(1..tree_grid.length - 2).each do |x|
  (1..tree_grid[0].length - 2).each do |y|
    visibility = visibility_from_tree([x, y], tree_grid)
    scenic_score = [scenic_score, visibility].max
  end
end

puts "Part 2: #{scenic_score}"
