# Advent of Code - Day 19, Year 2015
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2015/day/19
# Solution by: [abbasmoosajee07]
# Brief: [Chemistry and Strings]

require 'set'
require 'pathname'

# Load the input file
d19_file = 'Day19_input.txt'
d19_file_path = Pathname.new(__FILE__).dirname.join(d19_file)

molecules = File.readlines(d19_file_path).map(&:chomp)
molecule_p3 = molecules[-1]

def generate_replacements(string_to_replace, replace_with_string, molecule)
  # Generate all distinct replacements by replacing one occurrence at a time
  replacements = []
  offset = 0
  
  while (index = molecule.index(string_to_replace, offset))
    new_molecule = molecule.dup
    new_molecule[index, string_to_replace.length] = replace_with_string
    replacements << new_molecule
    offset = index + 1 # Move past the current index for the next search
  end

  replacements
end

def generate_molecule_tuple(list_of_molecules)
  molecule_tuple_list = []
  list_of_molecules.each do |item|
    match_data = item.match(/(\w+) => (\w+)/)
    if match_data
      molecule_tuple_list << [match_data[1], match_data[2]]
    end
  end
  molecule_tuple_list
end

rudy_medicine_molecules = molecules
molecule_to_change = rudy_medicine_molecules.pop # Get the last molecule (to change)
rudy_medicine_molecules.pop # Remove the empty line

molecule_tuples = generate_molecule_tuple(rudy_medicine_molecules)
distinct_molecules = Set.new

molecule_tuples.each do |item|
  list_of_potential_replacements = generate_replacements(item[0], item[1], molecule_to_change)
  distinct_molecules.merge(list_of_potential_replacements)
end

puts "Part 1: We have #{distinct_molecules.size} distinct molecules. \n"

molecule = molecule_p3
step_1 = molecule.gsub("Rn", '(')
step_2 = step_1.gsub('Ar', ')')
step_3 = step_2.gsub('Y', ',')

# puts step_3

left_parens = step_3.count("(")
right_parens = step_3.count(")")
commas = step_3.count(",")

# Count the total occurrences of the specified elements
total = step_3.scan(/Al|B|Ca|F|H|Mg|N|O|P|Si|Th|Ti/).size + left_parens + right_parens + commas

# Adjust the total based on parentheses and commas
equation = total - (left_parens + right_parens) - (2 * commas)

puts "Part 2: #{equation}"
