# Advent of Code - Day 22, Year 2016
# Solved in 2024
# Puzzle Link: https://adventofcode.com/2016/day/22
# Solution by: [abbasmoosajee07]
# Brief: [Creating a Node Map, Second variation]

import collections
import heapq
import re, os

P = collections.namedtuple('Point', ['x', 'y'])

class Point(P):
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

Origin = Point( 0,  0)
Up     = Point( 0, -1)
Down   = Point( 0,  1)
Left   = Point(-1,  0)
Right  = Point( 1,  0)

def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# Main Program
D22_file = 'Day22_input.txt'
D22_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D22_file)

LARGE = 0.5

DIRECTIONS = [Up, Down, Left, Right]


def parse_file(file):
  with open(file) as f:
    return sorted(tuple(int(n) for n in re.findall(r'\d+', line))
                  for line in f.read().strip().split('\n')
                  if line.startswith('/'))

def viable_pairs(tups):
  viable = 0
  for i, tup1 in enumerate(tups):
    for j, tup2 in enumerate(tups):
      if i == j:
        continue
      if 0 < tup1[3] <= tup2[4]:
        viable += 1
  return viable

real_tups = parse_file(D22_file_path)
# print(f"Day 22 part 1: {viable_pairs(real_tups)}")


State = collections.namedtuple("State", ['goal', 'hole', 'steps'])


class Grid:
  def __init__(self, file, threshold=LARGE, access_node=Origin):
    tups = parse_file(file)
    sizes = collections.Counter(tup[2] for tup in tups)
    useds = collections.Counter(tup[3] for tup in tups)
    assert useds[0] == 1, f'there are {useds[0]} holes but should be exactly 1'
    avails = collections.Counter(tup[4] for tup in tups if tup[3] > 0)
    assert max(avails.keys()) < max(k for k in useds.keys() if k > 0), 'aside from hole, every `used` should be greater than every `avail`'
    starting_hole_size = [tup[2] for tup in tups if tup[3] == 0][0]
    self.large_size = LARGE * max(sizes.keys())
    assert starting_hole_size < self.large_size, 'the hole should be a small node'

    self.nodes = set()
    self.access_node = access_node
    self.initial_goal_node = None
    self.initial_hole_node = None
    self.get_nodes(tups)
    self.adj = self.get_adjacency_lists()

  def get_nodes(self, tups):
    for tup in tups:
      if tup[2] > self.large_size:
        continue
      node = Point(tup[0], tup[1])
      self.nodes.add(node)
      self.better_goal_node(node)
      if tup[3] == 0:
        self.initial_hole_node = node

  def better_goal_node(self, node):
    if node.y == 0:
      if self.initial_goal_node is None or node.x > self.initial_goal_node.x:
        self.initial_goal_node = node

  def get_adjacency_lists(self):
    adj = collections.defaultdict(list)
    for node in self.nodes:
      for direction in DIRECTIONS:
        if (point := node + direction) in self.nodes:
          adj[node].append(point)
    return adj

  def solve(self):
    # get initial states for A* by calling self.bfs for self.adj[self.goal_node]
    priority_queue = []
    visited = set()
    for neighbor in self.adj[self.initial_goal_node]:
      steps = self.bfs(self.initial_hole_node, neighbor, self.initial_goal_node)
      # now switch goal and hole and increment steps
      steps += 1
      state = State(neighbor, self.initial_goal_node, steps)
      if (state.goal, state.hole) not in visited:
        heapq.heappush(priority_queue,
                       (steps + self.heuristic(neighbor), state))
        visited.add((state.goal, state.hole))

    while priority_queue:
      state = heapq.heappop(priority_queue)[1]
      if state.goal == self.access_node:
        return state.steps
      for neighbor in self.adj[state.goal]:
        steps = state.steps + self.bfs(state.hole, neighbor, state.goal) + 1
        new_state = State(neighbor, state.goal, steps)
        if (new_state.goal, new_state.hole) not in visited:
          heapq.heappush(priority_queue,
                         (steps + self.heuristic(neighbor), new_state))
          visited.add((new_state.goal, new_state.hole))

  def heuristic(self, node):
    result = 5 * manhattan_distance(node, self.access_node)
    if node.x != self.access_node.x and node.y != self.access_node.y:
      result -= 2  # hole takes only 3 steps to move around for turn
    return result

  def bfs(self, start, end, exclude=None):
    steps = 0
    visited = set()
    current = set()
    current.update(self.adj[start])
    if exclude is not None:
      visited.add(exclude)
      current.discard(exclude)
    pending = []
    while current:
      if end in visited:
        return steps
      for move in current:
        visited.add(move)
        for next_move in self.adj[move]:
          if next_move not in visited:
            pending.append(next_move)
      steps += 1
      current = set(pending)
      pending = []
    if end in visited:
      return steps


# test_grid = Grid(TEST_D22_file_path)
# assert test_grid.solve() == 7

real_grid = Grid(D22_file_path)
print(f"Day 22 part 2: {real_grid.solve()}")


