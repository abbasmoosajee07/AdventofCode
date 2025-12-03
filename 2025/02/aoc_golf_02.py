invalid_ids_p1 = 0
for id_range in open(0).read().split(","):
    id_start, id_end = map(int, id_range.split("-"))
    for test_id in range(id_start, id_end + 1):
        id_str = str(test_id)
        id_half = len(id_str) // 2
        if id_str[:id_half] == id_str[id_half:]:
            invalid_ids_p1 += test_id
print(invalid_ids_p1)

invalid_ids_p2 = 0
for id_range in open(0).read().split(","):
    id_start, id_end = map(int, id_range.split("-"))
    for test_id in range(id_start, id_end + 1):
        id_str = str(test_id)
        id_len = len(id_str)
        for pattern_len in range(id_len):
            if id_str.count(id_str[:pattern_len]) * pattern_len == id_len:
                invalid_ids_p2 += test_id
                break
print(invalid_ids_p2)
