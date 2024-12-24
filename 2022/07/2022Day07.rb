=begin
Advent of Code - Day 7, Year 2022
Solution Started: Nov 30, 2024
Puzzle Link: https://adventofcode.com/2022/day/7
Solution by: abbasmoosajee07
Brief: [Create File Tree]
=end

#!/usr/bin/env ruby

require 'pathname'

# Define file name and extract complete path to the input file
D07_file = "Day07_input.txt"
D07_file_path = Pathname.new(__FILE__).dirname + D07_file

# Read the input data
input_data = File.readlines(D07_file_path).map(&:strip)

def create_file_tree(command_list)
  sizes = Hash.new(0)
  stack = []

  command_list.each do |command|
    if command.start_with?("$ ls") || command.start_with?("dir")
      next
    elsif command.start_with?("$ cd")
      destination = command.split[2]
      if destination == ".."
        stack.pop
      else
        path = stack.empty? ? destination : "#{stack.last}_#{destination}"
        stack.push(path)
      end
    else
      size, _ = command.split
      stack.each { |path| sizes[path] += size.to_i }
    end
  end

  required_size = 30_000_000 - (70_000_000 - sizes["/"])
  ans_p2 = sizes.values.sort.find { |size| size > required_size }
  ans_p1 = sizes.values.select { |num| num <= 100_000 }.sum

  [ans_p1, ans_p2]
end

ans_p1, ans_p2 = create_file_tree(input_data)
puts "Part 1: #{ans_p1}"
puts "Part 2: #{ans_p2}"

