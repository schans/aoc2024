#!/usr/bin/env python3

import fileinput

# counters
T = 0

DIRS = {'>': (0, 1), '<': (0, -1), '^': (-1, 0), 'v': (1, 0)}
P = (0, 0)
I = ""
G = []
for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    if l.startswith('#'):
        G.append(list(l))
    else:
        I += l

R = len(G)
C = len(G[0])

for r in range(R):
    for c in range(C):
        if G[r][c] == '@':
            P = (r, c)
            G[r][c] = '.'
            break


def move(d):
    global G, P
    (dr, dc) = d

    (r, c) = P
    rr, cc = r+dr, c + dc

    # empty
    if G[rr][cc] == '.':
        P = (rr, cc)
        return

    # wall
    if G[rr][cc] == '#':
        return

    # move
    assert G[rr][cc] == 'O', ('unknown obstacle', G[rr][cc])

    nr, nc = rr, cc
    while True:
        nr, nc = nr+dr, nc + dc
        if G[nr][nc] == '#':
            # continues to wall
            return

        if G[nr][nc] == 'O':
            # skip to next
            continue

        if G[nr][nc] == '.':
            G[nr][nc] = 'O'
            G[rr][cc] = '.'
            P = (rr, cc)
            return


for i in I:
    move(DIRS[i])

for r in range(R):
    for c in range(C):
        if G[r][c] == 'O':
            T += r*100 + c

print(f"Tot {T}")
