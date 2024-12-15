#!/usr/bin/env python3

import fileinput

# counters
T = 0

DIRS = {'>': (0, 1), '<': (0, -1), '^': (-1, 0), 'v': (1, 0)}
P = (0, 0)
I = ""
G = []
W = set()
O = set()

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
        elif G[r][c] == 'O':
            O.add((r, c))
        elif G[r][c] == '#':
            W.add((r, c))


def move(d):
    global P, O, W
    (dr, dc) = d

    (r, c) = P
    rr, cc = r+dr, c + dc

    # empty
    if (rr, cc) not in W and (rr, cc) not in O:
        P = (rr, cc)
        return

    # wall
    if (rr, cc) in W:
        return

    # move
    assert (rr, cc) in O, ('unknown obstacle at', (rr, cc))

    def move_box(o, d):
        (dr, dc) = d
        (r, c) = o
        nr, nc = r+dr, c + dc

        if (nr, nc) in W:
            return False

        if (nr, nc) not in W and (nr, nc) not in O:
            O.remove(o)
            O.add((nr, nc))
            return True

        if (nr, nc) in O:
            if move_box((nr, nc), d):
                O.remove(o)
                O.add((nr, nc))
                return True
            else:
                return False
        assert False, 'no no'

    if move_box((rr, cc), d):
        P = (rr, cc)


for i in I:
    move(DIRS[i])

for (r, c) in O:
    T += r*100 + c

print(f"Tot {T}")
