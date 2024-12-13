#!/usr/bin/env pypy3

import fileinput

# counters
T = 0
T2 = 0

m = dict()
M = list()
for line in fileinput.input():
    l = line.strip()
    if not l:
        M.append(m)
        m = dict()
        continue

    if l.startswith("Button A"):
        p = l.split(':')
        x, y = l.split(':')[1].strip().split(', ')
        x = int(x[2:])
        y = int(y[2:])
        m['A'] = (x, y)

    if l.startswith("Button B"):
        p = l.split(':')
        x, y = l.split(':')[1].strip().split(', ')
        x = int(x[2:])
        y = int(y[2:])
        m['B'] = (x, y)

    if l.startswith("Prize:"):
        p = l.split(':')
        x, y = l.split(':')[1].strip().split(', ')
        x = int(x[2:])
        y = int(y[2:])
        m['P'] = (x, y)

# add last
M.append(m)


def tokens2(m):
    # Ax *k + Ay*k + Bx * j + By * j
    # Ax *k + Bx * j = X =>  Axk = X - Bxj => k = (X - Bxj) / Ax = X/Ax - Bxj/Ax
    # Ay *k + By * j = Y => Ayk = Y - Byj => k =  (Y- Byj) / Ay
    #
    # (Y-Byj)/Ay = (X-Bxj)/Ax
    # AxY- AxByj = AyX - AyBxj
    # AyBxj - AxByj = AyX - AxY
    # j (AyBx-AxBy) = (AyX - AxY)
    # j = (AyX - AxY) / (AyBx - AxBy)
    # j = (m['A'][1]*m['P'][0] - m['A'][0]*m['P'][1]) / (m['A'][1] * m['B'][0] - m['A'][0] * m['B'][1])
    above = (m['A'][1]*m['P'][0] - m['A'][0]*m['P'][1])
    below = (m['A'][1] * m['B'][0] - m['A'][0] * m['B'][1])
    if above % below == 0:

        j = above // below
        # k = (m['P'][1] - m['B'][1]*j) / m['A'][1]
        above = (m['P'][1] - m['B'][1]*j)
        below = m['A'][1]
        if above % below != 0:
            # not all j's work
            return 0
        k = above // below
        assert m['A'][0]*k + m['B'][0]*j == m['P'][0], 'wrong x'
        assert m['A'][1]*k + m['B'][1]*j == m['P'][1], 'wrong y'
        return 3*k + j
    return 0


for m in M:
    T += tokens2(m)
    (x, y) = m['P']
    x += 10000000000000
    y += 10000000000000
    m['P'] = (x, y)
    T2 += tokens2(m)

print(f"Tot {T} {T2}")
