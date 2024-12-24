=begin
Advent of Code - Day 24, Year 2024
Solution Started: Dec 24, 2024
Puzzle Link: https://adventofcode.com/2024/day/24
Solution by: abbasmoosajee07
Brief: [Code/Problem Description]
=end

#!/usr/bin/env ruby

require 'pathname'

# Define file name and extract complete path to the input file
D24_file = "Day24_input.txt"
D24_file_path = Pathname.new(__FILE__).dirname + D24_file

# Read the input data
input_data = File.readlines(D24_file_path).map(&:strip)

require 'set'

# Read input and parse
g = {}
File.read(D24_file_path).scan(/([a-z0-9]+) (AND|OR|XOR) ([a-z0-9]+) -> ([a-z0-9]+)/).each do |a, o, b, w|
  g[w] = [o, a, b]
end

c = g.keys.select { |w| w.match?(/^z[0-9]+$/) }.map { |w| w[1..].to_i }.max
m = 2**(c + 1) - 1

# Test function for single evaluation
def test1(e, x, y, s, g, c)
  v = {}

  (0...c).each do |i|
    v["x%02d" % i] = (x >> i) & 1
    v["y%02d" % i] = (y >> i) & 1
  end

  e.each do |w|
    o, a, b = g[s.fetch(w, w)]
    if o == "AND"
      v[w] = v[a] & v[b]
    elsif o == "OR"
      v[w] = v[a] | v[b]
    elsif o == "XOR"
      v[w] = v[a] ^ v[b]
    end
  end

  (0..c).each do |i|
    return i if v["z%02d" % i] != ((x + y) >> i) & 1
  end
  c + 1
end

# Test function for all evaluations
def testn(s, g, c, m)
  begin
    # Create a topological order
    e = []
    dependency_graph = {}
    g.each do |w, (_, a, b)|
      key = s.fetch(w, w)
      dependency_graph[key] ||= []
      dependency_graph[key] << a unless s.key?(a)
      dependency_graph[key] << b unless s.key?(b)
    end

    sorted = []
    visited = Set.new

    toposort = lambda do |node|
      raise 'CycleError' if visited.include?(node)
      return if sorted.include?(node)

      visited.add(node)
      if dependency_graph[node]
        dependency_graph[node].each { |child| toposort.call(child) }
      end
      visited.delete(node)
      sorted << node
    end

    g.keys.each { |node| toposort.call(node) unless sorted.include?(node) }
    e = sorted.select { |w| g.key?(w) }

    [[m, 0], [0, m], [m, 1], [1, m], [m, m]].map do |x, y|
      test1(e, x, y, s, g, c)
    end.min
  rescue
    0
  end
end

# Main logic for finding the result
s = {}
while s.size < 8
  pairs = g.keys.combination(2).select do |a, b|
    a < b && !s.key?(a) && !s.key?(b)
  end

  best_pair = pairs.max_by do |a, b|
    testn(s.merge({ a => b, b => a }), g, c, m)
  end

  s.merge!({ best_pair[0] => best_pair[1], best_pair[1] => best_pair[0] })
end

puts s.keys.sort.join(',')
