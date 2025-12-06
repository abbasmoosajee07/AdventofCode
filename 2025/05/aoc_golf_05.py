import sys
inp_data = sys.stdin.read().split("\n\n")
fresh_range = [tuple(map(int, id_range.split("-"))) for id_range in inp_data[0].split("\n")]

fresh_count = 0
for check_ing in list(map(int, inp_data[1].split("\n"))):
    for start, end in fresh_range:
        if start <= check_ing <= end:
            fresh_count += 1
            break
print(fresh_count)



import sys
fresh_range = [tuple(map(int, id_range.split("-"))) for id_range in sys.stdin.read().split("\n\n")[0].split("\n")]

sorted_range = sorted(fresh_range, key=lambda x: x[0])

merged_range = []
current_start, current_end = sorted_range[0]

for start, end in sorted_range[1:]:
    if start <= current_end + 1:
        current_end = max(current_end, end)
    else:
        merged_range.append((current_start, current_end))
        current_start, current_end = start, end

merged_range.append((current_start, current_end))

total = 0
for start, end in merged_range:
    total += (end - start) + 1

print(total)
