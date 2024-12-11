#!/usr/bin/env pypy3

import fileinput
from functools import cache

# counters
T = 0
T2 = 0

stones = []
for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    stones = [*map(int, l.split())]


@cache
def num_stones(s, n):
    if n == 0:
        return 1
    if s == 0:
        return num_stones(1, n-1)
    elif len(str(s)) % 2 == 0:
        ss = str(s)
        return num_stones(int(ss[:len(ss)//2]), n-1) + num_stones(int(ss[len(ss)//2:]), n-1)
    else:
        return num_stones(s * 2024, n-1)


T = sum([num_stones(s, 25) for s in stones])
T2 = sum([num_stones(s, 75) for s in stones])

print(f"Tot {T} {T2}")
