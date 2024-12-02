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
    if r != sorted(r) and r != sorted(r, reverse=True):
        return False
    for i in range(len(r)-1):
        d = abs(r[i]-r[i+1])
        if d < 1 or d > 3:
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
