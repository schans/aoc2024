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
            P = (r, 2*c)
        elif G[r][c] == 'O':
            O.add((r, 2*c))
        elif G[r][c] == '#':
            W.add((r, 2*c))
            W.add((r, 2*c+1))


def move(d):
    global P, O, W
    (dr, dc) = d

    (r, c) = P
    rr, cc = r+dr, c + dc

    # wall
    if (rr, cc) in W:
        return

    # empty
    if (rr, cc) not in W and (rr, cc) not in O and (rr, cc-1) not in O:
        P = (rr, cc)
        return

    # move
    assert (rr, cc) in O or (rr, cc-1) in O, ('unknown obstacle at', (rr, cc))

    def can_move_updown(o, d):
        (dr, dc) = d
        (r, c) = o
        nr, nc = r+dr, c + dc

        if o not in O:
            return True

        if (nr, nc) in W or (nr, nc+1) in W:
            return False

        if (nr, nc) not in O and (nr, nc-1) not in O and (nr, nc+1) not in O:
            return True

        if (nr, nc) in O:
            return can_move_updown((nr, nc), d)

        return can_move_updown((nr, nc-1), d) and can_move_updown((nr, nc+1), d)

    def move_box(o, d):
        assert o in O, "not found"
        (dr, dc) = d
        (r, c) = o
        nr, nc = r+dr, c + dc

        if d == (0, 1):
            if (nr, nc+1) in W:
                return False
            elif (nr, nc+1) not in O:
                O.remove(o)
                O.add((nr, nc))
                return True
            else:
                if move_box((nr, nc+1), d):
                    O.remove(o)
                    O.add((nr, nc))
                    return True
                else:
                    return False

        elif d == (0, -1):
            if (nr, nc) in W:
                return False
            elif (nr, nc-1) not in O:
                O.remove(o)
                O.add((nr, nc))
                return True
            else:
                if move_box((nr, nc-1), d):
                    O.remove(o)
                    O.add((nr, nc))
                    return True
                else:
                    return False
        else:
            if (nr, nc) in W or (nr, nc+1) in W:
                return False
            elif (nr, nc) not in O and (nr, nc+1) not in O and (nr, nc-1) not in O:
                O.remove(o)
                O.add((nr, nc))
                return True
            else:
                if (nr, nc) in O:
                    if move_box((nr, nc), d):
                        O.remove(o)
                        O.add((nr, nc))
                        return True
                    else:
                        return False
                else:
                    if can_move_updown((nr, nc-1), d) and can_move_updown((nr, nc+1), d):
                        if (nr, nc-1) in O:
                            move_box((nr, nc-1), d)
                        if (nr, nc+1) in O:
                            move_box((nr, nc+1), d)
                        O.remove(o)
                        O.add((nr, nc))
                        return True
                    else:
                        return False

    if (rr, cc) in O:
        if move_box((rr, cc), d):
            P = (rr, cc)
    else:
        if move_box((rr, cc-1), d):
            P = (rr, cc)


def dump():
    print('-'*24)
    for r in range(R):
        for c in range(C*2):
            if (r, c) == P:
                print('@', end="")
            elif (r, c) in O:
                print('[', end="")
            elif (r, c-1) in O:
                print(']', end="")
            elif (r, c) in W:
                print('#', end="")
            else:
                print('.', end="")
        print()


for i in I:
    move(DIRS[i])

for (r, c) in O:
    T += r*100 + c

print(f"Tot {T}")
