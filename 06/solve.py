#!/usr/bin/env python3

import fileinput

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

curp = (0, 0)
curd = 0

for r in range(R):
    for c in range(C):
        if G[r][c] == '^':
            curp = (r, c)
            break


def get_path_len(g, curp, curd):
    seen = set()
    while True:
        seen.add(curp)
        nr, nc = curp[0] + D[curd][0], curp[1]+D[curd][1]
        if nr < 0 or nr >= R or nc < 0 or nc >= C:
            break
        if g[nr][nc] == '#':
            curd = (curd+1) % len(D)
        else:
            curp = (nr, nc)
    return len(seen)


def check_loop(g, curp, curd):
    seen = set()
    while True:
        seen.add((curp, curd))
        nr, nc = curp[0] + D[curd][0], curp[1]+D[curd][1]
        if nr < 0 or nr >= R or nc < 0 or nc >= C:
            return False
        if g[nr][nc] == '#':
            curd = (curd+1) % len(D)
        else:
            curp = (nr, nc)
        if (curp, curd) in seen:
            return True


T = get_path_len(G, curp, curd)

for r in range(R):
    for c in range(C):
        if G[r][c] in '#^':
            continue
        G[r][c] = '#'
        if check_loop(G, curp, curd):
            T2 += 1
        G[r][c] = '.'


print(f"Tot {T} {T2}")
