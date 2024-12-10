#!/usr/bin/env python3

import fileinput
from collections import deque

# counters
T = 0
T2 = 0

TH = set()
G = []
for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    G.append([*map(int, l)])

R = len(G)
C = len(G[0])

for r in range(R):
    for c in range(C):
        if G[r][c] == 0:
            TH.add((r, c))


def bfs2(start):
    q = deque()
    q.append((start, frozenset()))
    nines = set()
    seen = set()

    while q:
        (r, c), path = q.pop()
        if G[r][c] == 9:
            nines.add(((r, c), path))
            continue

        if ((r, c), path) in seen:
            continue
        seen.add(((r, c), path))

        for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            rr = r + dr
            cc = c + dc
            if 0 <= rr < R and 0 <= cc < C and G[rr][cc] - G[r][c] == 1:
                pp = set(path)
                pp.add((rr, cc))
                pp = frozenset(pp)
                q.append(((rr, cc), pp))

    return len(nines)


def bfs(start):
    q = deque()
    q.append(start)
    nines = set()
    seen = set()

    while q:
        (r, c) = q.pop()
        if G[r][c] == 9:
            nines.add((r, c))
            continue

        if (r, c) in seen:
            continue
        seen.add((r, c))

        for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            rr = r + dr
            cc = c + dc
            if 0 <= rr < R and 0 <= cc < C and G[rr][cc] - G[r][c] == 1:
                q.append((rr, cc))

    return len(nines)


for tf in TH:
    T += bfs(tf)
    T2 += bfs2(tf)

print(f"Tot {T} {T2}")
