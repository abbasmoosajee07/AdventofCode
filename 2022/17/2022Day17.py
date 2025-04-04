"""Advent of Code - Day 17, Year 2022
Solution Started: Dec 7, 2024
Puzzle Link: https://adventofcode.com/2022/day/17
Solution by: abbasmoosajee07
Brief: [Tetris]
"""

#!/usr/bin/env python3

import os, re, copy, itertools
import time
from dataclasses import dataclass
from enum import Enum

# Load the input data from the specified file path
D17_file = "Day17_input.txt"
D17_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D17_file)

# Read and sort input data into a grid
with open(D17_file_path) as file:
    input_data = file.read().strip().split('\n')[0]

class ShapeType(Enum):
    """ Enum for our five shapes """
    HLINE =       {(0, 0), (1, 0), (2, 0), (3, 0)}
    PLUS =        {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)}
    BACKWARDS_L = {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)}
    I =           {(0, 0), (0, 1), (0, 2), (0, 3)}
    SQUARE =      {(0, 0), (1, 0), (0, 1), (1, 1)}    

MOVE = {
    "<": (-1, 0),
    ">": (1, 0),
    "V": (0, -1)
}

@dataclass(frozen=True)
class Point():
    """ Point with x,y coordinates and knows how to add a vector to create a new Point. """
    x: int
    y: int
    
    def __add__(self, other):
        """ Add other point/vector to this point, returning new point """
        return Point(self.x + other.x, self.y + other.y)     
        
    def __repr__(self) -> str:
        return f"P({self.x},{self.y})"
    
class Shape():
    """ Stores the points that make up this shape. 
    Has a factory method to create Shape instances based on shape type. """
    
    def __init__(self, points: set[Point], at_rest=False) -> None:
        self.points: set[Point] = points   # the points that make up the shape
        self.at_rest = at_rest
    
    @classmethod
    def create_shape_by_type(cls, shape_type: str, origin: Point):
        """ Factory method to create an instance of our shape.
        The shape points are offset by the supplied origin. """
        return cls({(Point(*coords) + origin) for coords in ShapeType[shape_type].value})

    @classmethod
    def create_shape_from_points(cls, points: set[Point], at_rest=False):
        """ Factory method to create an instance of our shape. """
        return cls(points, at_rest)
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Shape):
            return self.points == __o.points
        else:
            return NotImplemented  
    
    def __hash__(self) -> int:
        return hash(repr(self))

class Tower():
    """ Fixed width tower that generates new shapes to drop, and blows shapes left and right as they drop. """
    WIDTH = 7
    LEFT_WALL_X = 0  
    RIGHT_WALL_X = LEFT_WALL_X + 7 + 1  # right wall at x=8
    OFFSET_X = 2 + 1  # objects start with left edge at x=3
    OFFSET_Y = 3 + 1  # new rocks have a gap of 3 above top of highest settled rock
    FLOOR_Y = 0

    def __init__(self, jet_pattern: str) -> None:
        self._jet_pattern = itertools.cycle(enumerate(jet_pattern)) # infinite cycle
        self._shape_generator = itertools.cycle(enumerate(item.name for item in ShapeType))  # infinite cycle
        self.top = Tower.FLOOR_Y  # keep track of top of blocks
        self._all_at_rest_shapes: set[Shape] = set()
        self._all_at_rest_points: set[Point] = set() # tracking this for speed
        
        self.repeat_identified = False
        self._cache: dict[tuple, tuple] = {}    # K=(rock_idx, jet_idx, rock_formation): V=(height, shape_ct)
        self._repeat: tuple = (0, 0)  # height_diff, shape_diff
    
    def _current_origin(self) -> Point:
        """ Rocks are dropped 2 from the left edge, and 3 above the current tallest settled rock. """
        return Point(Tower.LEFT_WALL_X + Tower.OFFSET_X, self.top + Tower.OFFSET_Y)
    
    def _next_shape(self):
        """ Get the next shape from the generator """
        return next(self._shape_generator)
    
    def _next_jet(self):
        """ Get the next jet blast from the generator """
        return next(self._jet_pattern)
    
    def _check_cache(self, shape_index: int, jet_index: int, formation: str) -> tuple:
        key = (shape_index, jet_index, formation)
        shape_ct = len(self._all_at_rest_shapes)
        if key in self._cache: # We've found a repeat!
            last_height, last_shape_count = self._cache[key]
            return (True, self.top, last_height, shape_ct, last_shape_count)
        else: # cache miss, so add new entry to the cache
            self._cache[key] = (self.top, shape_ct)
            
        return (False, self.top, 0, shape_ct, 0)
    
    def drop_shape(self):
        shape_index, next_shape_type = self._next_shape()
        self.current_shape = Shape.create_shape_by_type(next_shape_type, self._current_origin())
            
        while True:
            jet_index, jet = self._next_jet()
            self._move_shape(jet)
            
            if not self._move_shape("V"): # failed to move down
                self.top = max(self.top, max(point.y for point in self.current_shape.points))
                settled_shape = Shape.create_shape_from_points(self.current_shape.points, True)
                self._settle_shape(settled_shape)
                if not self.repeat_identified:
                    cache_response = self._check_cache(shape_index, jet_index, self.get_recent_formation())
                    if cache_response[0]: # Cache hit
                        self.repeat_identified = True
                        self._repeat = (cache_response[1] - cache_response[2], # current top - last top
                                        cache_response[3] - cache_response[4]) # current shape ct - last shape ct

                break
    
    def calculate_height(self, shape_drops: int) -> tuple[int, int]:
        """ Calculate the additional height given n shape drops. """
        remaining_drops = shape_drops - len(self._all_at_rest_shapes)
        repeats_req = remaining_drops // self._repeat[1]    # full repeats
        remaining_drops %= self._repeat[1]      # remaining individual drops
        
        height_delta = self._repeat[0] * repeats_req  # height created by these repeats
        new_height = self.top + height_delta
        
        return new_height, remaining_drops
    
    def _settle_shape(self, shape: Shape):
        """ Add this shape to the settled sets """
        self._all_at_rest_shapes.add(shape)
        self._all_at_rest_points.update(shape.points)
    
    def _move_shape(self, direction) -> bool:
        """ Move a shape in the direction indicated. Return False if we can't move. """
        
        # Test against boundaries
        if direction == "<":
            shape_left_x = min(point.x for point in self.current_shape.points)
            if shape_left_x == Tower.LEFT_WALL_X + 1:
                return False # can't move left
            
        if direction == ">":
            shape_right_x = max(point.x for point in self.current_shape.points)
            if shape_right_x == Tower.RIGHT_WALL_X - 1:
                return False # can't move right
            
        if direction == "V":
            shape_bottom = min(point.y for point in self.current_shape.points)
            if shape_bottom == Tower.FLOOR_Y + 1:
                return False # can't move down
        
        # Move phase - test for collision
        candidate_points = {(point + Point(*MOVE[direction])) for point in self.current_shape.points}
        if self._all_at_rest_points & candidate_points: # If the candidate would intersect
            return False # Then this is not a valid position
        else: # We can move there. Update our current shape position, by constructing a new shape at the new position
            self.current_shape = Shape.create_shape_from_points(candidate_points)
        return True
    
    def get_recent_formation(self) -> str:
        """ Covert last (top) 20 rows into a str representation. """
        rows = []
        min_y = max(0, self.top-20) # we want the last 20 lines
        for y in range(min_y, self.top+1):
            line = ""
            for x in range(Tower.LEFT_WALL_X, Tower.RIGHT_WALL_X):
                if Point(x,y) in self._all_at_rest_points:
                    line += "#"
                elif Point(x,y) in self.current_shape.points:
                    line += "@"
                else:
                    line += "."
            rows.append(line)
            
        return "\n".join(rows[::-1])
    def __repr__(self) -> str:
        return (f"Tower(height={self.top}, rested={len(self._all_at_rest_shapes)})")
    def final_height(self) -> int:
        return(self.top)

tower = Tower(jet_pattern=input_data)
for _ in range(2022):
    tower.drop_shape()

height_p1 = tower.final_height()
print(f"Part 1: {height_p1}")

# Part 2
tower = Tower(jet_pattern=input_data)  # Recreate the initial tower
while not tower.repeat_identified:  # Drop until we identify the first repeat
    tower.drop_shape()
height_at_repeat_start = tower.top  # The height achieved before first repeat

new_height, remaining_drops = tower.calculate_height(1000000000000)
for _ in range(remaining_drops):
    tower.drop_shape()
height_after_top_up = tower.top
height_p2 = new_height + height_after_top_up - height_at_repeat_start

print(f"Part 2: {height_p2}")

