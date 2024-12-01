#!/usr/bin/env pypy3

import fileinput
from collections import defaultdict

# counters
T = 0
T2 = 0


L = []
R = []
F = defaultdict(int)
for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    le, ri = l.split()
    L.append(int(le))
    R.append(int(ri))
    F[int(ri)] += 1

L.sort()
R.sort()

for i in range(len(L)):
    T += abs(L[i] - R[i])
    T2 += L[i] * F[L[i]]

print(f"Tot {T} {T2}")
