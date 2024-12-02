#!/usr/bin/env pypy3

import fileinput
from collections import defaultdict

# counters
T = 0
T2 = 0


R = []
for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    R.append([int(c) for c in l.split()])


def is_valid(r):
    d = r[1] - r[0]
    if d == 0:
        return False
    for i in range(len(r)-1):
        c = r[i+1]-r[i]
        if d > 0 and (c < 1 or c > 3):
            return False
        if d < 0 and c > -1 or c < -3:
            return False
    return True


for r in R:
    if is_valid(r):
        T += 1
        T2 += 1
    else:
        for i in range(len(r)):
            t = r.copy()
            t.pop(i)
            if is_valid(t):
                T2 += 1
                break

print(f"Tot {T} {T2}")
