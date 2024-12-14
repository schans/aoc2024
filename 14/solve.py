#!/usr/bin/env pypy3

import fileinput
from collections import defaultdict

# counters
T = 0
T2 = 0

X = 101
Y = 103

R = list()

for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    r = dict()
    p, v = l.split()
    p = p[2:]
    v = v[2:]
    p = [int(c) for c in p.split(',')]
    v = [int(c) for c in v.split(',')]
    r['p'] = p
    r['v'] = v
    R.append(r)


def dump():
    p = set()
    for r in R:
        p.add(tuple(r['p']))
    for x in range(X):
        for y in range(Y):
            if (x, y) in p:
                print('*', end='')
            else:
                print('.', end='')
        print()


def quarters():
    Q = defaultdict(int)
    for r in R:
        if 0 <= r['p'][0] < X//2 and 0 <= r['p'][1] < Y//2:
            # top left
            Q[0] += 1
        elif X//2 < r['p'][0] < X and 0 <= r['p'][1] < Y//2:
            # top right
            Q[1] += 1
        elif X//2 < r['p'][0] < X and Y//2 < r['p'][1] < Y:
            # botom right
            Q[2] += 1
        elif 0 <= r['p'][0] < X//2 and Y//2 < r['p'][1] < Y:
            # bottom left
            Q[3] += 1
    return Q


found = False
for i in range(1, 10**6):
    p = set()
    for r in R:
        r['p'][0] += r['v'][0]
        r['p'][1] += r['v'][1]
        r['p'][0] %= X
        r['p'][1] %= Y
        p.add(tuple(r['p']))

    if i == 100:
        Q = quarters()
        T = Q[0] * Q[1] * Q[2] * Q[3]

    # check if robots form long line
    for x in range(X):
        row = 0
        for y in range(Y):
            if (x, y) in p:
                row += 1
                if row > 28:
                    T2 = i
                    found = True
                    break
            else:
                row = 0

    if found:
        break

print(f"Tot {T} {T2}")
