map_dict = {
    (row_no, col_no): cell
    for row_no, row_data in enumerate(open(0))
    for col_no, cell in enumerate(row_data)
}

queue = [next(pos for pos, cell in map_dict.items() if cell == 'S')]
visited = set()
split_count = 0
while queue:
    beam_pos = queue.pop()
    beam_row, beam_col = beam_pos
    if beam_pos in visited:
        continue
    visited.add(beam_pos)
    map_cell = map_dict.get(beam_pos, ' ')
    if map_cell in '.S':
        queue.append((beam_row + 1, beam_col))
    elif map_cell == '^':
        split_count += 1
        queue.append((beam_row, beam_col + 1))
        queue.append((beam_row, beam_col - 1))
print(split_count)


map_dict = {
    (row_no, col_no): cell
    for row_no, row_data in enumerate(open(0))
    for col_no, cell in enumerate(row_data)
}

from functools import lru_cache

@lru_cache(maxsize=None)
def count_from(pos, depth=0):
    if depth > 1000:
        return 0

    cell = map_dict.get(pos)
    if cell is None:
        return 1

    if cell in '.S':
        return count_from((pos[0] + 1, pos[1]), depth + 1)
    elif cell == '^':
        left = count_from((pos[0], pos[1] - 1), depth + 1)
        right = count_from((pos[0], pos[1] + 1), depth + 1)
        return left + right
    return 0

print(count_from(next(pos for pos, cell in map_dict.items() if cell == 'S')))