=begin
Advent of Code - Day 4, Year 2024
Solution Started: Dec 4, 2024
Puzzle Link: https://adventofcode.com/2024/day/4
Solution by: abbasmoosajee07
Brief: [Code/Problem Description]
=end

#!/usr/bin/env ruby

require 'pathname'

# Define file name and extract complete path to the input file
D04_file = "Day04_input.txt"
D04_file_path = Pathname.new(__FILE__).dirname + D04_file

# Read and sort input data into a grid
input_data = File.read(D04_file_path).strip.split("\n")
word_grid = input_data.map { |row| row.chars }

def is_valid?(x, y, size_x, size_y)
  x >= 0 && x < size_x && y >= 0 && y < size_y
end

def search_word(grid, word, result_grid, directions = "Both")
  n, m = grid.size, grid[0].size
  word_count = 0 # Count instances of the word

  cardinal_directions = [[1, 0], [0, -1], [0, 1], [-1, 0]] # Cardinal directions
  diagonal_directions = [[1, 1], [1, -1], [-1, 1], [-1, -1]] # Diagonal directions

  directions = case directions.downcase
              when "both"
                cardinal_directions + diagonal_directions
              when "cardinal"
                cardinal_directions
              when "diagonals"
                diagonal_directions
              else
                raise ArgumentError, "Invalid direction: #{directions}"
              end

  (0...n).each do |i|
    (0...m).each do |j|
      # Check if the first character matches
      if grid[i][j] == word[0]
        directions.each do |dir_x, dir_y|
          if find_word_in_direction(grid, n, m, word, i, j, dir_x, dir_y)
            result_grid = mark_word_in_grid(result_grid, word, i, j, dir_x, dir_y)
            word_count += 1 # Increment word count
          end
        end
      end
    end
  end

  return result_grid, word_count
end

def find_word_in_direction(grid, n, m, word, i, j, dir_x, dir_y)
  # Check if all characters of the word are within bounds and match
  (0...word.length).each do |k|
    new_row = i + dir_x * k
    new_col = j + dir_y * k

    # If the new position is out of bounds, return false
    return false unless (0 <= new_row && new_row < n && 0 <= new_col && new_col < m)

    # If the character does not match, return false
    return false if grid[new_row][new_col] != word[k]
  end

  # If all characters match, return true
  true
end

def mark_word_in_grid(result_grid, word, start_row, start_col, dir_x, dir_y)
  # Mark the found word in the result grid
  (0...word.length).each do |k|
    new_row = start_row + dir_x * k
    new_col = start_col + dir_y * k
    result_grid[new_row][new_col] = word[k]
  end
  result_grid
end
def count_word_instances(word_words, grid, directions = "both")
  found_grid = Array.new(grid.size) { Array.new(grid[0].size, '.') } # Initialize grid with '.'
  total_count = 0

  word_words.each do |word|
    unless word.empty?
      found_grid, word_count = search_word(grid, word, found_grid, directions)
      total_count += word_count
    end
  end

  return total_count, found_grid
end


target_words_p1 = ["XMAS"]
grid_p1 = Marshal.load(Marshal.dump(word_grid)) # Deep copy of the grid
word_count_p1, found_grid_p1 = count_word_instances(target_words_p1, grid_p1)
puts "Part 1: #{word_count_p1}"

def count_diagonal_word_matches(grid, target_words)
  y_size, x_size = grid.size, grid[0].size
  count = 0
  target_word_list = [target_words[0], target_words[0].reverse]

  (1...(y_size - 1)).each do |y|
    (1...(x_size - 1)).each do |x|
      # Extract diagonals
      d1 = grid[y - 1][x - 1] + grid[y][x] + grid[y + 1][x + 1]  # Top-left to bottom-right
      d2 = grid[y + 1][x - 1] + grid[y][x] + grid[y - 1][x + 1]  # Top-right to bottom-left

      # Check if either diagonal matches the target word or its reverse
      if target_word_list.include?(d1) && target_word_list.include?(d2)
        count += 1
      end
    end
  end

  count
end

target_words_p2 = ["MAS"]
grid_p2 = Marshal.load(Marshal.dump(word_grid)) # Deep copy of the grid
word_count_p2, found_grid_p2 = count_word_instances(target_words_p2, grid_p2, directions = "diagonals")
count_p2 = count_diagonal_word_matches(found_grid_p2, target_words_p2)

puts "Part 2: #{count_p2}"
