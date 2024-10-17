def get_next_coordinates(row: int, col: int):
    """Compute the next row and column in the sequence based on current row and column."""
    return (col + 1, 1) if row == 1 else (row - 1, col + 1)


def compute_next_code(current_code: int):
    """Generate the next code using the modular arithmetic provided."""
    return (current_code * 252533) % 33554393


def next_step(row: int, col: int, current_code: int):
    """Calculate the next row, column, and code."""
    next_row, next_col = get_next_coordinates(row, col)
    next_code = compute_next_code(current_code)
    return next_row, next_col, next_code


# Initialize variables
code, row, col = 27995004, 6, 6

# Continue until the target coordinates are reached
while (row, col) != (2981, 3075):
    row, col, code = next_step(row, col, code)

print(f"The input of the puzzle: {code}")