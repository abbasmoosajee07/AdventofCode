# Advent of Code - Day 20, Year 2020
# Solution Started: Nov 22, 2024
# Puzzle Link: https://adventofcode.com/2020/day/20
# Solution by: [abbasmoosajee07]
# Brief: [Arranging grids]

#!/usr/bin/env python3

import os, re, copy
import numpy as np
from math import prod
from scipy.ndimage import convolve

# Load the input data from the specified file path
D20_file = "Day20_input.txt"
D20_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), D20_file)

# Read and sort input data into a grid
with open(D20_file_path) as file:
    input_data = file.read().strip().split('\n\n')

def create_grid_list(input):
    grid_list = []
    for grid_entry in input:
        tile, grid = grid_entry.split(':')
        grid_array = np.array([list(row) for row in grid.split('\n') if list(row) != []])
        tile_no = int(tile.strip('Tile '))
        grid_list.append([tile_no, grid_array])
    return grid_list

# Extract edges
def get_edges(tile_grid):
    """Returns all edges (and their reversed versions) of a tile grid."""
    top = tile_grid[0, :]
    bottom = tile_grid[-1, :]
    left = tile_grid[:, 0]
    right = tile_grid[:, -1]
    return [top, right, bottom, left, top[::-1], right[::-1], bottom[::-1], left[::-1]]

# Find matching tiles
def find_matching_tiles(grid_list):
    """Finds tiles that share edges and returns a mapping."""
    edge_map = {}  # Maps edge to the tiles that have it
    tile_edges = {}  # Maps tile number to its edges

    for tile_id, grid in grid_list:
        edges = get_edges(grid)
        tile_edges[tile_id] = edges
        for edge in edges:
            edge_str = ''.join(edge)
            if edge_str not in edge_map:
                edge_map[edge_str] = []
            edge_map[edge_str].append(tile_id)
    
    # Find neighbors for each tile
    matches = {}
    for tile_id, edges in tile_edges.items():
        matches[tile_id] = []
        for edge in edges:
            edge_str = ''.join(edge)
            # Find other tiles that share this edge
            neighbors = [t for t in edge_map[edge_str] if t != tile_id]
            matches[tile_id].extend(neighbors)
    return matches

# Identify corner tiles
def find_corner_tiles(matches):
    """Finds tiles with exactly 2 matches (corner tiles)."""
    return [tile for tile, neighbors in matches.items() if len(set(neighbors)) == 2]

# Main function to solve the puzzle

# Find tile matches
grid_list = create_grid_list(input_data)
tile_matches = find_matching_tiles(grid_list)

# Part 1: Identify corner tiles and multiply their IDs
corner_tiles = find_corner_tiles(tile_matches)
corner_product = prod(corner_tiles)
print(f"Part 1: {corner_product}")

T = [lambda x:x[:],
     lambda x:x.T[::-1],
     lambda x:x[::-1,::-1],
     lambda x:x[::-1].T,
     lambda x:x[::-1],
     lambda x:x.T,
     lambda x:x[:,::-1],
     lambda x:x[::-1,::-1].T]

model=np.array([[1,2],[3,4]])
ref = {tuple(tr(model).flat):k for k,tr in enumerate(T)}
Tmul = np.array([[ref[tuple(tb(ta(model)).flat)] for tb in T] for ta in T])
Tinv = np.argwhere(Tmul==0)[:,1]

def parse(photo):
    photo=photo.replace("#","1").replace(".","0")
    header,*pixels=photo.split("\n")
    id_=int(header[5:-1])
    pixels=np.array([list(p) for p in pixels])
    edges=[int("".join(tr(pixels)[0]),2) for tr in T]
    return id_,pixels.astype(int),edges

def populate(ps,links,i_dest0,trans0,i_src0):
    for dir_,index_diff in enumerate([-12,1,12,-1]):
        edge_out0=Tmul[trans0,dir_]
        i_src1,edge_match1=links[i_src0,edge_out0]
        i_dest1=i_dest0+index_diff
        if i_src1>-1 and -1<i_dest1<len(ps) and ps[i_dest1][0]==-1:
            trans_fit1=Tmul[edge_match1,Tinv[(edge_out0+4)%8]]
            trans1=Tmul[trans_fit1,trans0]
            ps[i_dest1]=trans1,i_src1
            populate(ps,links,i_dest1,trans1,i_src1)

def answers(raw):
    ids,pixels,edges=map(np.array,zip(*map(parse,raw)))
    L=len(edges)

    ms=np.argwhere(edges[:,:,None,None]==edges)
    ms=ms[ms[:,0]!=ms[:,2]]
    links=np.full((L,8,2),-1)
    links[tuple(ms[:,:2].T)]=ms[:,2:]

    ps=np.full((2*L,2),-1)
    ps[L]=0,0
    populate(ps,links,L,0,0)
    ps=ps[ps[:,0]!=-1]

    yield np.prod(ids[ps[[0,11,-12,-1],1]],dtype=np.int64)

    tr_pixels=[T[tr](pixels[i_src])[1:-1,1:-1] for tr,i_src in ps]
    full_image=np.reshape(tr_pixels,(12,12,8,8))
    full_image=np.moveaxis(full_image,2,1).reshape(96,96)
    kernel=["                  #  ",
            "#    ##    ##    ### ",
            " #  #  #  #  #  #    "]
    kernel=(np.array([list(row) for row in kernel])=="#").astype(int)
    N=kernel.sum()
    matches=[convolve(full_image,tr(kernel),mode="constant")==N for tr in T]
    
    yield np.sum(full_image)-np.sum(matches)*N


results = list(answers(input_data))
print(f"Part 2: {results[1]}")

