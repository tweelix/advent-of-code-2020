import pyparsing as pp
from collections import defaultdict
from itertools import product
from copy import deepcopy

e = pp.Char("e")
w = pp.Char("w")
se = pp.Combine(pp.Group(pp.Char("s") + e))
sw = pp.Combine(pp.Group(pp.Char("s") + w))
nw = pp.Combine(pp.Group(pp.Char("n") + w))
ne = pp.Combine(pp.Group(pp.Char("n") + e))


parser = pp.OneOrMore(se | sw | nw | ne | e | w)

with open("input") as f:
    directions = [parser.parseString(line).asList() for line in f.readlines()]

black_tiles = 0
reference_tile = (0, 0)
tiles = defaultdict(lambda: "w")
directions_lut = {
    "e": (1, 0),
    "w": (-1, 0),
    "se": (0, 1),
    "sw": (-1, 1),
    "ne": (1, -1),
    "nw": (0, -1),
}
for instructions in directions:
    current_tile = reference_tile
    for direction in instructions:
        transform = directions_lut[direction]
        current_tile = (current_tile[0] + transform[0], current_tile[1] + transform[1])
    if tiles[current_tile] == "w":
        tiles[current_tile] = "b"
        black_tiles += 1
    else:
        tiles[current_tile] = "w"
        black_tiles -= 1
print("Task 1:", black_tiles)


max_q = max(tile[0] for tile in tiles.keys())
min_q = min(tile[0] for tile in tiles.keys())
max_r = max(tile[1] for tile in tiles.keys())
min_r = min(tile[1] for tile in tiles.keys())

def iterate_over_6_directions(coords):
    for transform in directions_lut.values():
        yield (coords[0] + transform[0], coords[1] + transform[1])


for i in range(100):
    tiles_to_flip = []
    max_q += 1
    min_q -= 1
    max_r += 1
    min_r -= 1
    for q, r in product(range(min_q, max_q + 1), range(min_r, max_r + 1)):
        neighbours = 0
        for _q, _r in iterate_over_6_directions((q, r)):
            if tiles[(_q, _r)] == "b":
                neighbours += 1
                if neighbours > 2:
                    break
        if (neighbours == 2 and tiles[(q, r)] == "w") or (
            (neighbours == 0 or neighbours > 2) and tiles[(q, r)] == "b"
        ):
            tiles_to_flip.append((q, r))
    max_q_count = 0
    max_r_count = 0
    min_q_count = 0
    min_r_count = 0
    for coords in tiles_to_flip:
        if tiles[coords] == "w":
            tiles[coords] = "b"
            black_tiles += 1
            if coords[0] == max_q:
                max_q_count += 1
            if coords[0] == min_q:
                min_q_count += 1
            if coords[1] == max_r:
                max_r_count += 1
            if coords[1] == min_r:
                min_r_count += 1
        else:
            tiles[coords] = "w"
            black_tiles -= 1
    if max_r_count == 0:
        max_r -= 1
    if min_r_count == 0:
        min_r += 1
    if max_q_count == 0:
        max_q -= 1
    if min_q_count == 0:
        min_q += 1

print("Task 2:", black_tiles)
