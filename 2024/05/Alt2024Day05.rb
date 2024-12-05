=begin
Advent of Code - Day 5, Year 2024
Solution Started: Dec 5, 2024
Puzzle Link: https://adventofcode.com/2024/day/5
Solution by: abbasmoosajee07
Brief: [Validating Reports]
=end

#!/usr/bin/env ruby

require 'pathname'

# Define file name and extract complete path to the input file
D05_file = "Day05_input.txt"
D05_file_path = Pathname.new(__FILE__).dirname + D05_file

# Read and split the input data into sections
input_data = File.read(D05_file_path).strip.split("\n\n")

# Function to apply rules to the given book list
def apply_rule(book, rules)
  # Check if any rule applies; return 0 if true, otherwise return the middle element of the book list
  rules.each do |rule|
    if book.include?(rule[0]) && book.include?(rule[1]) &&
       book.index(rule[0]) > book.index(rule[1])
      return 0
    end
  end
  return book[book.length / 2]
end

# Function to swap elements in the book list based on rules
def swap_elements(book, rules)
  rules.each do |rule|
    if book.include?(rule[0]) && book.include?(rule[1]) &&
       book.index(rule[0]) > book.index(rule[1])
      # Swap the elements in the book list
      index_0, index_1 = book.index(rule[0]), book.index(rule[1])
      book[index_0], book[index_1] = book[index_1], book[index_0]
      return true
    end
  end
  return false
end

# Main function to calculate the results for Part 1 and Part 2
def calculate_results(rules, update_list)
  mid_p1 = 0
  mid_p2 = 0

  update_list.each do |book|
    res = apply_rule(book, rules)
    mid_p1 += res

    # For Part 2, apply the rule multiple times if the result is 0
    if res == 0
      while swap_elements(book, rules)
        mid_p2 += apply_rule(book, rules)
      end
    end
  end

  return mid_p1, mid_p2
end

# Convert the input data to the appropriate format
manual_dict = input_data[0].split("\n").map { |line| line.split('|').map(&:to_i) }
update_list = input_data[1].split("\n").map { |line| line.split(',').map(&:to_i) }

# Calculate and print the results for both parts
ans_p1, ans_p2 = calculate_results(manual_dict, update_list)
puts "Part 1: #{ans_p1}"
puts "Part 2: #{ans_p2}"
