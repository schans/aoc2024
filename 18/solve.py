#!/usr/bin/env pypy3

import fileinput
from heapq import heapify, heappop, heappush

# counters
T = 0
T2 = 0

O = list()
DIRS = ((0, 1), (0, -1), (-1, 0), (1, 0))
R = 70 + 1
C = 70 + 1
B = 1024

start = (0, 0)
end = (R-1, C-1)

for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    c, r = [int(c) for c in l.split(',')]
    O.append((r, c))


def dump(bytes):
    print('-'*24)
    for r in range(R):
        for c in range(C):
            if (r, c) in bytes:
                print('#', end="")
            else:
                print('.', end="")
        print()
    print('-'*24)


def dijkstra(start, end, bytes):
    pq = [(0, start)]
    heapify(pq)
    seen = set()

    while pq:
        (d, p) = heappop(pq)

        if p == end:
            return d
        if p in seen:
            continue
        seen.add(p)

        (r, c) = p
        for (dr, dc) in DIRS:
            rr, cc = r+dr, c+dc
            if 0 <= rr < R and 0 <= cc < C and (rr, cc) not in bytes:
                heappush(pq, (d+1, (rr, cc)))

    return -1


def get_bytes(mb):
    return set((O[i] for i in range(mb+1)))


bytes = get_bytes(B)
T = dijkstra(start, end, bytes)

for i in range(B-1, len(O)):
    bytes = get_bytes(i)
    t = dijkstra(start, end, get_bytes(i))
    if t == -1:
        T2 = str(O[i][1]) + ',' + str(O[i][0])
        break

print(f"Tot {T} {T2}")
