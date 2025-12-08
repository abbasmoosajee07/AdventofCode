import math
total_sum = 0
sheet_grid = [row.split() for row in open(0)]
for problem in [[row[i] for row in sheet_grid] for i in range(len(sheet_grid[0]))]:
    problem_ints =  list(map(int, problem[:-1]))
    total_sum += math.prod(problem_ints) if problem[-1] == '*' else sum(problem_ints)
print(total_sum)

from sys import stdin

lines = stdin.readlines()
max_len = max(len(row) for row in lines)

padded_sheet = [row + " " * (max_len - len(row)) for row in lines]

total_sum = 0
current_problem = operation = None

for col_idx in range(max_len):
    column = [row[col_idx] for row in padded_sheet]

    if all(cell == " " for cell in column):
        total_sum += current_problem
        current_problem = operation = None
        continue

    digits = [cell for cell in column if cell.isdigit()]
    operators = [cell for cell in column if cell in "+*"]

    if digits:
        number = int("".join(digits))

        if current_problem is None:
            current_problem = number
        elif operation == "+":
            current_problem += number
        elif operation == "*":
            current_problem *= number
        else:
            current_problem = number

    if operators:
        operation = operators[0]

print(total_sum + current_problem)