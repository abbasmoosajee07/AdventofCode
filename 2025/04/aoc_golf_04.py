
grid_p1 = {
    (row_no, col_no): cell == '@'
    for row_no, row_data in enumerate(open(0))
    for col_no, cell in enumerate(row_data)
}
accescible_rolls_p1 = 0
for r, c in grid_p1:
    papers = 0
    for dr, dc in [(0, 1), (0, -1), (-1, 0), (1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
        if grid_p1.get((r + dr, c + dc)):
            papers += 1
    if grid_p1[r, c] and papers < 4:
        accescible_rolls_p1 += 1
print(accescible_rolls_p1)


grid_p2 = {
    (row_no, col_no): cell == '@'
    for row_no, row_data in enumerate(open(0))
    for col_no, cell in enumerate(row_data)
}
accescible_rolls = 1
papers_moved = 0
while accescible_rolls != 0:
    accescible_rolls = 0
    for pos in grid_p2:
        r, c = pos
        papers = 0
        for dr, dc in [(0, 1), (0, -1), (-1, 0), (1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            if grid_p2.get((r + dr, c + dc)):
                papers += 1
        if grid_p2[pos] and papers < 4:
            accescible_rolls += 1
            papers_moved += 1
            grid_p2[pos] = False
print(papers_moved)

