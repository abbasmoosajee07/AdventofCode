require 'enumerator'

# Function to calculate the ingredient score
def ingredient_score(teaspoon_list, ingredient_list)
  combined_list = teaspoon_list.zip(ingredient_list)
  total_ingredients = []

  combined_list.each do |teaspoons, ingredient|
    temp_list = ingredient.map { |prop| prop.to_i * teaspoons }
    total_ingredients << temp_list
  end

  properties = total_ingredients.transpose
  final_score = 1
  property_count = 1  # This is to ignore calories for part 1

  properties.each do |cookie_property|
    sum_property = cookie_property.sum
    final_score *= sum_property if sum_property > 0
    property_count += 1
    break if property_count == 5
  end

  final_score
end

# Function to parse the ingredient input
def parse_ingredients(ingredient_inputs)
  pattern = /(-*\d)/
  ingredient_inputs.map { |ingredient| ingredient.scan(pattern).flatten }
end

# Brute force to find the best cookie score
def brute_force_cookie_score(ingredient_list)
  ingredient_combos = (1..99).to_a.permutation(ingredient_list.size).select { |combo| combo.sum == 100 }
  
  max_score = 0
  ingredient_combos.each do |ingredient_combination|
    combo_score = ingredient_score(ingredient_combination, ingredient_list)
    max_score = combo_score if combo_score > max_score
  end
  max_score
end

# Input ingredients as a list of strings
input = [
  "Frosting: capacity 4, durability -2, flavor 0, texture 0, calories 5",
  "Candy: capacity 0, durability 5, flavor -1, texture 0, calories 8",
  "Butterscotch: capacity -1, durability 0, flavor 5, texture 0, calories 6",
  "Sugar: capacity 0, durability 0, flavor -2, texture 2, calories 1"
]

if __FILE__ == $0
  ingredients = parse_ingredients(input)
  cookie_score = brute_force_cookie_score(ingredients)
  puts "The cookie score is #{cookie_score}"
end
