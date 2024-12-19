#!/usr/bin/env pypy3

import fileinput
from functools import cache

# counters
T = 0
T2 = 0


P = list()
L = list()
for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    if not P:
        P = l.split(', ')
    else:
        L.append(l)


@cache
def match_all(s):
    if s == "":
        return 1
    else:
        r = 0
        for p in P:
            if s.startswith(p):
                r += match_all(s[len(p):])
        return r


for s in L:
    n = match_all(s)
    if n:
        T += 1
    T2 += n

print(f"Tot {T} {T2}")
