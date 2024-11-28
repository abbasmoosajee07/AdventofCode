# Advent of Code - Day 3, Year 2022
# Solution Started: Nov 28, 2024
# Puzzle Link: https://adventofcode.com/2022/day/3
# Solution by: [abbasmoosajee07]
# Brief: [Rucksacks and Unique Letters]

require 'set'

# Load the input data from the specified file path
D03_file = "Day03_input.txt"
D03_file_path = File.join(File.dirname(File.expand_path(__FILE__)), D03_file)

# Read and sort input data into a grid
input_data = File.readlines(D03_file_path).map(&:strip)

def split_str_in_middle(str)
  # Convert str to list
  lst = str.chars
  # Calculate the middle index
  mid = lst.length / 2
  # Split the list into two halves
  [lst[0...mid], lst[mid..-1]]
end

def calc_total_priority(rucksack_list)
  lowercase_priority = Hash[("a".."z").to_a.zip(1..26)] # Generate lowercase letters and their priorities
  uppercase_priority = Hash[("A".."Z").to_a.zip(27..52)] # Generate uppercase letters and their priorities
  # Merging dictionaries using merge
  letter_priority = lowercase_priority.merge(uppercase_priority)

  total_priorities = 0
  rucksack_list.each do |rucksack|
    compartment_1, compartment_2 = split_str_in_middle(rucksack)
    # Find common letters in both compartments
    common_letters = compartment_1 & compartment_2
    common_letters.each do |key|
      total_priorities += letter_priority[key]
    end
  end
  total_priorities
end

ans_p1 = calc_total_priority(input_data)
puts "Part 1: #{ans_p1}"

def calc_priority_grouped_elves(rucksack_list, group_by = 1)
  lowercase_priority = Hash[("a".."z").to_a.zip(1..26)] # Generate lowercase letters and their priorities
  uppercase_priority = Hash[("A".."Z").to_a.zip(27..52)] # Generate uppercase letters and their priorities
  # Merging dictionaries using merge
  letter_priority = lowercase_priority.merge(uppercase_priority)

  total_priorities = 0
  rucksack_list.each_slice(group_by) do |grouped_rucksacks|
    count_list = grouped_rucksacks.map { |rucksack| rucksack.chars.tally }
    
    # Find the intersection of all dictionaries (keys that are present in all)
    common_keys = count_list[0].keys.to_set
    count_list[1..-1].each do |count|
      common_keys &= count.keys.to_set
    end
    
    # Add the priorities for the common keys
    common_keys.each do |key|
      total_priorities += letter_priority[key] || 0
    end
  end
  total_priorities
end

ans_p2 = calc_priority_grouped_elves(input_data, group_by = 3)
puts "Part 2: #{ans_p2}"
