#!/usr/bin/env python3

import fileinput

# counters
T = 0
T2 = 0


G = []
for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    G.append(l)

R = len(G)
C = len(G[0])

def check_word_dir(r,c,dr,dc, w):
    rr,cc = r, c
    for i in range(0, len(w)):
        if not (0<=rr<R and 0<=cc<C):
            return 0
        elif G[rr][cc] != w[i]:
            return 0
        rr+= dr
        cc+= dc
    return 1

def check_word(r,c, w):
    dirs = [(0,1),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(1,0),(1,1)]
    return sum([check_word_dir(r,c, dr,dc, w) for (dr,dc) in dirs])


def check_cross(r,c, w):
    if not (1<=r<R-1 and 1<=c<C-1):
        return False
    t = 0
    for dr, dc in [(1,-1),(-1,-1),(-1,1),(1,1)]:
        nr = r+dr
        nc = c+dc
        t+=check_word_dir(nr,nc, -1*dr,-1*dc, w)
    return 1 if t == 2 else 0

for r in range(R):
    for c in range(C):
        if G[r][c] == 'X':
            T += check_word(r,c, "XMAS")
        elif G[r][c] == 'A':
            T2 += check_cross(r,c, "MAS")


print(f"Tot {T} {T2}")
