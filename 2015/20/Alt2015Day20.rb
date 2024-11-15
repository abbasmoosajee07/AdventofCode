# Advent of Code - Day 20, Year 2015
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2015/day/20
# Solution by: [abbasmoosajee07]
# Brief: [Chemistry and Strings]

def find_valid_multiples(number)
  """Find all valid multiples of the given number, including 1 to the number itself."""
  multiples = []
  (1..number).each do |i|
    multiples << i if number % i == 0  # Check if i is a divisor of the number
  end
  multiples
end

def multiply_elements(input_array, multiplier)
  """Multiply each element in the array by the given multiplier."""
  input_array.map { |element| element * multiplier }  # Using map for conciseness
end

gifts_per_house = 10
target_no = 36000000
gift_count = 0
house_no = 0

while gift_count < target_no
  house_no += 1
  elves_visiting = find_valid_multiples(house_no)
  gift_list = multiply_elements(elves_visiting, gifts_per_house)
  gift_count = gift_list.sum
  puts "House #{house_no} receives a total of #{gift_count} gifts."
end

puts "House #{house_no} receives a total of #{gift_count} gifts."
