# Advent of Code - Day 15, Year 2015
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2015/day/15
# Solution by: [abbasmoosajee07]
# Brief: [Constrained and Unconstrained Minima Problems]

# Function to parse the ingredients
def parse_ingredients(ingredient_inputs)
  pattern = /(-*\d+)/
  ingredient_inputs.map do |ingredient|
    ingredient.scan(pattern).flatten.map(&:to_i)
  end
end

# Function to calculate the ingredient score
def ingredient_score(teaspoon_list, ingredient_list)
  total_ingredients = ingredient_list.each_with_index.map do |ingredient, index|
    ingredient.map { |prop| prop * teaspoon_list[index] }
  end

  # Sum properties and calculate the final score
  properties_sum = total_ingredients.transpose.map(&:sum)
  final_score = 1

  properties_sum[0..3].each do |property_sum|  # Ignore calories (5th element)
    final_score *= [property_sum, 0].max  # If negative, set to 0
  end

  final_score
end

# Function to count calories
def count_calories(teaspoon_list, ingredient_list)
  teaspoon_list.each_with_index.sum do |teaspoons, index|
    teaspoons * ingredient_list[index][-1]  # Last element is calories
  end
end

# Brute force to find the best cookie score
def brute_force_cookie_score(ingredient_list, max_calorie)
  max_score = 0
  max_score_with_calories = 0
  
  # Generate all permutations where the sum of teaspoons is 100
  (1..99).to_a.permutation(ingredient_list.size).each do |combination|
    next unless combination.sum == 100  # Ensure sum of teaspoons is 100
    
    # Calculate scores for the current combination
    combo_score = ingredient_score(combination, ingredient_list)
    calorie_score = count_calories(combination, ingredient_list)

    # Update max score without calorie restriction
    max_score = [max_score, combo_score].max

    # Update max score with calorie restriction of exactly as defined
    if combo_score > max_score_with_calories && calorie_score == max_calorie
      max_score_with_calories = combo_score
    end
  end

  [max_score, max_score_with_calories]
end

# Input ingredients
input = [
  "Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8",
  "Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3"
]

# Main execution
if __FILE__ == $0
  ingredients = parse_ingredients(input)
  max_score, max_score_with_calories = brute_force_cookie_score(ingredients, 500)
  puts "The maximum cookie score is #{max_score}"
  puts "The maximum cookie score with 500 calories is #{max_score_with_calories}"
end
