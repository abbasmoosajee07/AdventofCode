
map_dict_p1 = {}
for row_no, row_data in enumerate(open(0)):
    for col_no, cell in enumerate(row_data):
        if cell == 'S':
            start_pos = row_no, col_no
        map_dict_p1[row_no, col_no] = cell
queue = [start_pos]
visited = set()
split_count = 0
while queue:
    beam_pos = queue.pop()
    beam_row, beam_col = beam_pos
    if beam_pos in visited:
        continue
    visited.add(beam_pos)
    map_cell = map_dict_p1.get(beam_pos, ' ')
    if map_cell in '.S':
        queue.append((beam_row + 1, beam_col))
    elif map_cell == '^':
        split_count += 1
        queue.append((beam_row, beam_col + 1))
        queue.append((beam_row, beam_col - 1))
print(split_count)


map_dict_p2 = {}
for row_no, row_data in enumerate(open(0)):
    for col_no, cell in enumerate(row_data):
        if cell == 'S':
            start_pos = row_no, col_no
        map_dict_p2[row_no, col_no] = cell

from functools import lru_cache

@lru_cache()
def count_from(pos, depth=0):
    row, col = pos
    depth += 1
    cell = map_dict_p2.get(pos)
    if cell is None:
        return 1
    if cell in '.S':
        return count_from((row+ 1, col), depth)
    elif cell == '^':
        left = count_from((row, col - 1), depth)
        right = count_from((row, col + 1), depth)
        return left + right
    return 0

print(count_from(start_pos))
