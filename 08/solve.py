#!/usr/bin/env pypy3

import fileinput
from collections import defaultdict

# counters
T = 0
T2 = 0


A = set()
A2 = set()
N = defaultdict(list)
R = C = 0

for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    C = len(l)
    R = fileinput.lineno()

    for c in range(len(l)):
        if l[c] != '.':
            N[l[c]].append((R-1, c))


for c in N:
    if len(N[c]) > 1:
        for cn in N[c]:
            for rn in N[c]:
                if cn != rn:
                    dr, dc = rn[0] - cn[0], rn[1] - cn[1]
                    an = (cn[0]-dr, cn[1]-dc)
                    if 0 <= an[0] < R and 0 <= an[1] < C:
                        A.add(an)

                    for i in range(-1 * max(R, C), max(R, C)):
                        an = (cn[0]-i*dr, cn[1]-i*dc)
                        if 0 <= an[0] < R and 0 <= an[1] < C:
                            A2.add(an)

T = len(A)
T2 = len(A2)
print(f"Tot {T} {T2}")
