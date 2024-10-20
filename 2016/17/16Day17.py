import hashlib
from collections import deque

input_str = "pslxynzg"

def hash_md5(s):
    return hashlib.md5(s.encode()).hexdigest()

def is_valid_location(x, y):
    return 0 <= x < 4 and 0 <= y < 4

def move(direction, x, y):
    if direction == 'U':
        return x, y - 1
    elif direction == 'D':
        return x, y + 1
    elif direction == 'L':
        return x - 1, y
    elif direction == 'R':
        return x + 1, y

def directions(path):
    hashed = hash_md5(input_str + path)
    open_doors = []
    if hashed[0] in "bcdef":
        open_doors.append('U')
    if hashed[1] in "bcdef":
        open_doors.append('D')
    if hashed[2] in "bcdef":
        open_doors.append('L')
    if hashed[3] in "bcdef":
        open_doors.append('R')
    return open_doors

def next_states(state):
    x, y, path = state
    if (x, y) == (3, 3):
        return []
    new_states = []
    for direction in directions(path):
        new_x, new_y = move(direction, x, y)
        if is_valid_location(new_x, new_y):
            new_states.append((new_x, new_y, path + direction))
    return new_states

def bfs(start):
    queue = deque([start])
    paths = []
    while queue:
        state = queue.popleft()
        if state[:2] == (3, 3):  # Reached the goal
            paths.append(state)
        queue.extend(next_states(state))
    return paths

def main():
    initial_state = (0, 0, "")
    paths = [(x, y, path) for x, y, path in bfs(initial_state)]
    shortest_path = paths[0][2]  # first path is the shortest
    longest_path = paths[-1][2]  # last path is the longest
    print(shortest_path)
    print(len(longest_path))

if __name__ == "__main__":
    main()
