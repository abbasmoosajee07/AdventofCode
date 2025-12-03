
jolts_p1 = 0
for battery in open(0).read().splitlines():
    memory = [0] * 3
    for bat in battery:
        memory = [0] + [
            max(memory[n + 1], memory[n] * 10 + int(bat))
            for n in range(2)
        ]
    jolts_p1 += memory[2]
print(jolts_p1)

jolts_p2 = 0
for battery in open(0).read().splitlines():
    memory = [0] * 13
    for bat in battery:
        memory = [0] + [
            max(memory[n + 1], memory[n] * 10 + int(bat))
            for n in range(12)
        ]
    jolts_p2 += memory[12]
print(jolts_p2)