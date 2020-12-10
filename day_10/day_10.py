from collections import Counter
from functools import reduce
from itertools import accumulate

with open("input") as f:
    input = [int(line) for line in f.readlines()]
input.extend([0, max(input)+3])

counts = Counter([j-i for i, j in zip(sorted(input)[:-1], sorted(input)[1:])])
print("part 1:", (counts[1]) * (counts[3]))

input_set = set(input)
combinations = reduce(lambda x, n: [sum(x) if n in input_set else 0, x[0], x[1]], range(1, max(input)+1), [1,0,0])[0]
print("part 2:", combinations)