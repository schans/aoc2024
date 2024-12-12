#!/usr/bin/env python3

import fileinput
from collections import deque

# counters
T = 0
T2 = 0

D = [(-1, -0), (0, 1), (1, 0), (0, -1)]

G = []
for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    G.append(list(l))

R = len(G)
C = len(G[0])

SEEN = set()

REGIONS = list()


def bfs(r, c):
    rv = G[r][c]
    queue = deque()
    queue.append((r, c))

    region = set()
    while queue:
        (r, c) = queue.popleft()
        if (r, c) in SEEN:
            continue
        SEEN.add((r, c))
        region.add((r, c))
        for (dr, dc) in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            rr, cc = r+dr, c + dc
            if 0 <= rr < R and 0 <= cc < C and G[rr][cc] == rv:
                queue.append((rr, cc))
    return region


def edges(region):
    e = 0
    for (r, c) in region:
        rv = G[r][c]
        for (dr, dc) in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            rr, cc = r+dr, c + dc
            if 0 <= rr < R and 0 <= cc < C:
                if G[rr][cc] != rv:
                    e += 1
            else:
                e += 1
    return e


def corners(region):
    x = 0
    for (r, c) in region:
        rv = G[r][c]
        top = right = bottom = left = '%'
        if 0 <= r-1 < R:
            top = G[r-1][c]
        if 0 <= r+1 < R:
            bottom = G[r+1][c]
        if 0 <= c-1 < C:
            left = G[r][c-1]
        if 0 <= c+1 < C:
            right = G[r][c+1]

        # 4x outer corner
        if rv != left and rv != top:
            x += 1
        if rv != top and rv != right:
            x += 1
        if rv != right and rv != bottom:
            x += 1
        if rv != bottom and rv != left:
            x += 1

        # 4x innter corner
        if rv == top == right:
            if 0 <= r-1 < R and 0 <= c+1 < C:
                if G[r-1][c+1] != rv:
                    x += 1
        if rv == right == bottom:
            if 0 <= r+1 < R and 0 <= c+1 < C:
                if G[r+1][c+1] != rv:
                    x += 1
        if rv == bottom == left:
            if 0 <= r+1 < R and 0 <= c-1 < C:
                if G[r+1][c-1] != rv:
                    x += 1
        if rv == left == top:
            if 0 <= r-1 < R and 0 <= c-1 < C:
                if G[r-1][c-1] != rv:
                    x += 1
    return x


for r in range(R):
    for c in range(C):
        if (r, c) in SEEN:
            continue
        REGIONS.append(bfs(r, c))

for r in REGIONS:
    a = len(r)
    e = edges(r)
    c = corners(r)
    T += a*e
    T2 += a*c


print(f"Tot {T} {T2}")
