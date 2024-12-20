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
    D = list()
    W = set()

    for p in P:
        (r, c) = p
        q = deque()
        q.append((0, p))
        seen = set()

        while q:
            d, (r, c) = q.popleft()
            if d >= max_cheat:
                continue

            if (r, c) in seen:
                continue
            seen.add((r, c))

            for (dr, dc) in DIRS:
                rr, cc = r+dr, c+dc
                if 0 <= rr < R and 0 <= cc < C:
                    q.append((d+1, (rr, cc)))
                    if G[rr][cc] != '#':
                        diff = P[p] - P[(rr, cc)] - (d+1)
                        if diff > 0 and (p, (rr, cc)) not in W and ((rr, cc), p) not in W:
                            W.add((p, (rr, cc)))
                            D.append(diff)

    # counting
    num = 0
    count = Counter(D)
    for k, v in count.items():
        if k >= 100:
            num += v
    return num


T = get_cheats(2)
T2 = get_cheats(20)

print(f"Tot {T} {T2}")
