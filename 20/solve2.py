#!/usr/bin/env python3

import fileinput
from collections import Counter, deque

# counters
T = 0
T2 = 0

DIRS = ((0, 1), (0, -1), (-1, 0), (1, 0))
S = E = (0, 0)
G = []
P = dict()

for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    G.append(list(l))

R = len(G)
C = len(G[0])


for r in range(R):
    for c in range(C):
        if G[r][c] == 'E':
            E = (r, c)
        if G[r][c] == 'S':
            S = (r, c)

# get step cost map
(r, c) = E
k = 0
P[E] = 0
while True:
    if (r, c) == S:
        break
    for (dr, dc) in DIRS:
        rr, cc = r+dr, c+dc
        if G[rr][cc] != '#' and (rr, cc) not in P:
            k += 1
            P[(rr, cc)] = k
            r, c = rr, cc
            break


def get_cheats(max_cheat):
    num = 0
    for (sr, sc) in reversed(P.keys()):
        for (er, ec) in P.keys():
            if (sr, sc) == (er, ec):
                break
            l = abs(sr-er)+abs(sc-ec)
            if l <= max_cheat and P[(sr, sc)] - P[(er, ec)] - l >= 100:
                num += 1
    return num


T = get_cheats(2)
T2 = get_cheats(20)

print(f"Tot {T} {T2}")
