# Template for reading all lines from stdin and printing the line count to stdout.
# Copy this code to your IDE to get started.

ps_p1=0
idx_p1=50
for rule in open(0):
    idx_p1 += int(rule[1:]) * (1 if rule[0] == "R" else -1)
    idx_p1 %= 100
    if idx_p1==0:
        ps_p1+=1
print(ps_p1)

ps_p2= 0
idx_p2=50
for rule in open(0):
    for _ in range(int(rule[1:])):
        idx_p2 += 1 if rule[0] == "R" else -1
        idx_p2 %= 100
        if idx_p2 == 0:
            ps_p2 += 1
print(ps_p2)
