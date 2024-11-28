# Advent of Code - Day 4, Year 2022
# Solution Started: Nov 28, 2024
# Puzzle Link: https://adventofcode.com/2022/day/4
# Solution by: abbasmoosajee07
# Brief: [Overlapping Number Sets]

require 'pathname'
require 'set'

# Define file name and extract complete  path to the input file,
D04_file = "Day04_input.txt"
D04_file_path = Pathname.new(__FILE__).dirname + D04_file

# Read the input data
input_data = File.readlines(D04_file_path).map(&:strip)

def form_assignment_sets(input_list)
  elves_list = []
  for line in input_list
    elf_1, elf_2 = line.split(',')

    elf_1_set = Set.new()
    elf_n11, elf_n12 = elf_1.split('-')
    elf_n11.to_i.upto(elf_n12.to_i) do |n1|
      elf_1_set.add(n1)
    end

    elf_2_set = Set.new()
    elf_n21, elf_n22 = elf_2.split('-')
    elf_n21.to_i.upto(elf_n22.to_i) do |n2|
      elf_2_set.add(n2)
    end

    elves_list << [elf_1_set, elf_2_set]
  end
  return elves_list
end

# Main execution
if __FILE__ == $0
  elves_sets = form_assignment_sets(input_data)

  fully_contained_sets = 0
  overlapping_len = 0
  for group in elves_sets
    elf_1 = group[0]
    elf_2 = group[1]
    if elf_1.superset?(elf_2) or elf_2.superset?(elf_1)
      fully_contained_sets += 1
    end
    overlapping_sets = elf_1 & elf_2
    if overlapping_sets.size != 0
      overlapping_len += 1
    end
  end
  puts "Part 1: #{fully_contained_sets}"
  puts "Part 2: #{overlapping_len}"
end
