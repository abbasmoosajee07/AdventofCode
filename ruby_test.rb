# Function to check if a number is prime
def prime?(number)
  return false if number <= 1
  (2..Math.sqrt(number)).none? { |i| number % i == 0 }
end

# Testing the prime? function
test_numbers = [1, 2, 3, 4, 5, 16, 17, 18, 19, 20]

test_numbers.each do |num|
  if prime?(num)
    puts "#{num} is a prime number."
  else
    puts "#{num} is not a prime number."
  end
end
