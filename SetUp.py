import subprocess

# Step 1: Create and write an R script
r_script = """
# Simple R script
x <- c(1, 2, 3, 4, 5)
y <- x^2
print(paste("Squares of x:", paste(y, collapse = " ")))
"""

with open("script.R", "w") as file:
    file.write(r_script)

# Step 2: Run the R script
print("Running R script...")
subprocess.run(["Rscript", "script.R"])

# Step 3: Create and write a Ruby script
ruby_script = """
# Simple Ruby script
x = [1, 2, 3, 4, 5]
y = x.map { |n| n ** 3 }
puts "Cubes of x: #{y.join(' ')}"
"""

with open("script.rb", "w") as file:
    file.write(ruby_script)

# Step 4: Run the Ruby script
print("Running Ruby script...")
subprocess.run(["ruby", "script.rb"])

# Step 5: Continue in Python
print("Back to Python!")
x = [1, 2, 3, 4, 5]
y = [i ** 4 for i in x]
print(f"Fourth powers of x: {y}")
