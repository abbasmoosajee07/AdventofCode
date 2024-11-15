# Advent of Code - Day 14, Year 2016
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2016/day/14
# Solution by: [abbasmoosajee07]
# Brief: [Extendng hascodes]

require 'digest'
require 'pathname'

# Define the file path
D14_file = 'Day14_input.txt'
D14_file_path = Pathname.new(__FILE__).dirname + D14_file

# Function to generate the stretched MD5 hash
def stretched_hash(input, cache, stretch)
  return cache[input] if cache[input]

  hash = Digest::MD5.hexdigest(input)
  stretch.times do
    hash = Digest::MD5.hexdigest(hash)
  end
  cache[input] = hash # Store the result in cache to reuse later
  hash
end

# Function to find 64th key index (with key stretching)
def find_64th_key(salt, stretch, target_key = 64)
  keys = []
  index = 0
  stretched_hash_cache = {} # Initialize the cache inside the function

  while keys.size < target_key
    # Generate stretched MD5 hash for the current index
    hash = stretched_hash("#{salt}#{index}", stretched_hash_cache, stretch)

    # Find triples in the hash (e.g. '777')
    if triple = hash[/(.)\1\1/]
      char = triple[0]

      # Check the next 1000 hashes for quintuples (e.g. '77777')
      (index + 1).upto(index + 1000) do |future_index|
        future_hash = stretched_hash("#{salt}#{future_index}", stretched_hash_cache, stretch)
        if future_hash.include?(char * 5)
          keys << index
          # puts "Key ##{keys.size}: Index #{index} (Hash: #{hash})"
          break
        end
      end
    end

    index += 1
  end

  keys.last # Return the 64th key index
end

# Read the contents of the file
# Puzzle input salt
salt = File.read(D14_file_path).strip
puts "----------------------""Part 1----------------------"
puts "The 64th key index is: #{find_64th_key(salt, 0)}"
puts "----------------------""Part 2----------------------"
puts "The 64th key index is: #{find_64th_key(salt, 2016)}"
