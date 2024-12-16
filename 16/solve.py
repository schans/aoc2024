#!/usr/bin/env python3

import fileinput
from heapq import heapify, heappop, heappush
from collections import deque

# counters
T = 0
T2 = 0

DIRS = {'e': (0, 1), 'w': (0, -1), 'n': (-1, 0), 's': (1, 0)}
TURNS = {'e': ('n', 's'), 'w': ('s', 'n'), 'n': ('e', 'w'), 's': ('w', 'e')}

G = []
for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    G.append(l)

R = len(G)
C = len(G[0])


def solve(g, start, end):
    q = list()
    d = 'e'
    q.append((0, d, start))
    heapify(q)
    seen = set()
    while q:
        (k, d, p) = heappop(q)
        if p == end:
            return k

        if (d, p) in seen:
            continue
        seen.add((d, p))

        (r, c) = p
        rr, cc = r + DIRS[d][0], c + DIRS[d][1]
        if g[rr][cc] != '#':
            heappush(q, (k+1, d, (rr, cc)))

        for dd in TURNS[d]:
            heappush(q, (k+1000, dd, (r, c)))

    assert False, 'lost in maze'


def solve2(g, start, end, maxk):
    q = list()
    pd = '#'
    d = 'e'
    q.append((0, d, pd, start, frozenset(start)))
    heapify(q)
    seen = dict()
    seen_path = set()
    while q:
        (k, d, pd, p, t) = heappop(q)
        if k > maxk:
            continue

        if p == end:
            assert k == maxk, "wrong cost"
            seen_path |= t
            continue

        if (d, pd, p) in seen:
            if k > seen[(d, pd, p)]:
                continue
        seen[(d, pd, p)] = k

        (r, c) = p
        rr, cc = r + DIRS[d][0], c + DIRS[d][1]
        if g[rr][cc] != '#':
            tt = set(t)
            tt.add((rr, cc))
            heappush(q, (k+1, d, pd, (rr, cc), frozenset(tt)))

        for dd in TURNS[d]:
            heappush(q, (k+1000, dd, p, (r, c), t))

    return len(seen_path)-1


start = end = (0, 0)
for r in range(R):
    for c in range(C):
        if G[r][c] == 'S':
            start = (r, c)
        if G[r][c] == 'E':
            end = (r, c)

T = solve(G, start, end)
T2 = solve2(G, start, end, T)
print(f"Tot {T} {T2}")
