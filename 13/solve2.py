#!/usr/bin/env python3

import fileinput
from re import findall
from z3 import *

# counters
T = 0
T2 = 0
M = list()


def ints(s):
    return list(map(int, findall(r'\d+', s)))


m = dict()
for line in fileinput.input():
    l = line.strip()

    if l.startswith("Button A"):
        m['ax'], m['ay'] = ints(l)
    elif l.startswith("Button B"):
        m['bx'], m['by'] = ints(l)
    elif l.startswith("Prize:"):
        m['px'], m['py'] = ints(l)

    if not l:
        M.append(m)
        m = dict()

M.append(m)


def tokens2(m):
    x = Int('x')
    y = Int('y')
    s = Solver()
    s.add(m['ax'] * x + m['bx'] * y == m['px'])
    s.add(m['ay'] * x + m['by'] * y == m['py'])
    if s.check() == sat:
        zm = s.model()
        return 3*zm[x].as_long() + zm[y].as_long()
    return 0


for m in M:
    T += tokens2(m)
    m['px'] += 10000000000000
    m['py'] += 10000000000000
    T2 += tokens2(m)

print(f"Tot {T} {T2}")
