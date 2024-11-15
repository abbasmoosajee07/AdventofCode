# Advent of Code - Day 11, Year 2018
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2018/day/11
# Solution by: [abbasmoosajee07]
# Brief: [Choral Elves, but faster]

SIZE = 300
serial = 9221

# Initialize the power grid with the given serial number
power = Array.new(SIZE) { Array.new(SIZE) }

# Calculate the power for each cell in the grid
(0...SIZE).each do |y|
  (0...SIZE).each do |x|
    rack = x + 1 + 10  # rack ID calculation (x + 1 because we use 0-based indexing)
    my_power = (rack * (y + 1) + serial) * rack  # y + 1 for 1-based y-coordinate
    my_power = (my_power / 100) % 10
    power[y][x] = my_power - 5
  end
end

# Find the maximum power for a 3x3 square
max_power = -Float::INFINITY
max_coords = []

(0...(SIZE - 2)).each do |y|
  (0...(SIZE - 2)).each do |x|
    total_power = 0
    # Sum of 3x3 square
    (0..2).each do |dy|
      (0..2).each do |dx|
        total_power += power[y + dy][x + dx]
      end
    end

    if total_power > max_power
      max_power = total_power
      max_coords = [x + 1, y + 1]  # Convert to 1-based indexing
    end
  end
end

puts "Coordinates: #{max_coords[0]}, #{max_coords[1]} with maximum power: #{max_power}"

# Now calculate the maximum power for any square size (from 1x1 to SIZE x SIZE)
sum_grid = Array.new(SIZE + 1) { Array.new(SIZE + 1, 0) }

# Calculate the prefix sum grid
(1..SIZE).each do |y|
  (1..SIZE).each do |x|
    sum_grid[y][x] = power[y - 1][x - 1] + sum_grid[y - 1][x] + sum_grid[y][x - 1] - sum_grid[y - 1][x - 1]
  end
end

max_power_any = -Float::INFINITY
max_coords_any = []
max_size = 0

# Iterate over all possible subgrid sizes
(1..SIZE).each do |subgrid_size|
  (1..(SIZE - subgrid_size + 1)).each do |ymin|
    ymax = ymin + subgrid_size - 1
    (1..(SIZE - subgrid_size + 1)).each do |xmin|
      xmax = xmin + subgrid_size - 1
      power_here = sum_grid[ymax][xmax] - sum_grid[ymin - 1][xmax] - sum_grid[ymax][xmin - 1] + sum_grid[ymin - 1][xmin - 1]

      if power_here > max_power_any
        max_power_any = power_here
        max_coords_any = [xmin, ymin, subgrid_size]
        # puts "Coordinates: #{max_coords_any[0]}, #{max_coords_any[1]} with size #{max_coords_any[2]} and maximum power: #{max_power_any}"
      end
    end
  end
end

puts "Coordinates: #{max_coords_any[0]}, #{max_coords_any[1]} with size #{max_coords_any[2]} and maximum power: #{max_power_any}"
