=begin
Advent of Code - Day 14, Year 2024
Solution Started: Dec 14, 2024
Puzzle Link: https://adventofcode.com/2024/day/14
Solution by: abbasmoosajee07
Brief: [Find Easter Egg]
=end

#!/usr/bin/env ruby

require 'pathname'
require 'set'
require 'csv'

# Define file name and extract complete path to the input file
D14_file = "Day14_input.txt"
D14_file_path = Pathname.new(__FILE__).dirname + D14_file

# Read and sort input data into a grid
input_data = File.read(D14_file_path).strip.split("\n")

GRID_SIZE = [101, 103]
X, Y = GRID_SIZE
DIRS = [[-1, 0], [1, 0], [0, -1], [0, 1]]  # Directions for BFS

def parse_input(particle_list)
  # Parse the input data into a dictionary of particles
  particle_dict = {}
  particle_list.each_with_index do |particle_properties, particle_no|
    p_x, p_y, v_x, v_y = particle_properties.scan(/-?\d+/).map(&:to_i)
    particle_dict[particle_no] = { 'p_x' => p_x, 'p_y' => p_y, 'v_x' => v_x, 'v_y' => v_y }
  end
  particle_dict
end

def update_particle_position(properties, grid_size = GRID_SIZE)
  # Update a particle's position based on its velocity
  properties['p_x'] += properties['v_x']
  properties['p_y'] += properties['v_y']
  properties['p_x'] %= grid_size[0]
  properties['p_y'] %= grid_size[1]
end

def calculate_safety_score(particles, grid_size = GRID_SIZE)
  # Calculate the safety score based on particle positions in quadrants
  quadrant_counts = [0, 0, 0, 0]  # Quadrant counts: [Q1, Q2, Q3, Q4]

  particles.each_value do |properties|
    final_x, final_y = properties['p_x'], properties['p_y']

    # Exclude midpoint
    next if final_x == grid_size[0] / 2 || final_y == grid_size[1] / 2

    # Correct quadrant assignment
    if final_x < grid_size[0] / 2 && final_y < grid_size[1] / 2
      quadrant_counts[0] += 1  # Quadrant 1
    elsif final_x > grid_size[0] / 2 && final_y < grid_size[1] / 2
      quadrant_counts[1] += 1  # Quadrant 2
    elsif final_x < grid_size[0] / 2 && final_y > grid_size[1] / 2
      quadrant_counts[2] += 1  # Quadrant 3
    elsif final_x > grid_size[0] / 2 && final_y > grid_size[1] / 2
      quadrant_counts[3] += 1  # Quadrant 4
    end
  end

  # Safety score is the product of particles in each quadrant
  quadrant_counts.reduce(1) { |acc, count| acc * count }
end

def find_connected_components(grid)
  # Find the number of connected components of particles in the grid
  components = 0
  seen = Set.new

  # BFS to find connected components
  X.times do |x|
    Y.times do |y|
      next if grid[y][x] != '#' || seen.include?([x, y])

      components += 1
      queue = [[x, y]]

      until queue.empty?
        x2, y2 = queue.shift
        next if seen.include?([x2, y2])

        seen.add([x2, y2])

        DIRS.each do |dx, dy|
          xx, yy = x2 + dx, y2 + dy
          queue << [xx, yy] if xx.between?(0, X-1) && yy.between?(0, Y-1) && grid[yy][xx] == '#'
        end
      end
    end
  end

  components
end

def visualize_particles(grid, time_step, file_path = 'grid_output.txt')
  # Visualize the grid and append it to a text file
  time_step_header = "\n--- Time Step #{time_step} ---\n"

  # Convert the grid into a string representation
  text_grid = grid.map { |row| row.join('') }.join("\n")

  # Append the grid for this time step to the file
  File.open(file_path, 'a') do |file|
    file.write(time_step_header)
    file.write(text_grid)
    file.write("\n")  # Add an empty line after each time step grid for separation
  end

  puts "Grid for time step #{time_step} saved to #{file_path}"
end

particles = parse_input(input_data)

easter_egg = nil

(1..(GRID_SIZE[0] * GRID_SIZE[1])).each do |min|
  # Update positions for the next time step
  particles.each_value do |properties|
    update_particle_position(properties, GRID_SIZE)
  end

  # Calculate safety score
  safety_score = calculate_safety_score(particles, GRID_SIZE)

  if min == 100  # Part 1 time
    puts "Part 1: #{safety_score}"
  end

  # Check for fewer than 200 connected components
  grid = Array.new(Y) { Array.new(X, ' ') }
  particles.each_value do |properties|
    x, y = properties['p_x'], properties['p_y']
    grid[y][x] = '#'
  end

  components = find_connected_components(grid)

  # Track the minimum safety score and time step with fewer than 200 components
  if components <= 200
    easter_egg = true
    puts "Part 2: #{min}"
    break
  end
end

puts "Part 2: No Christmas Tree Found" if easter_egg.nil?
