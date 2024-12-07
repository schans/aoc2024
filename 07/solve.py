#!/usr/bin/env pypy3

import fileinput

# counters
T = 0
T2 = 0


R = []
for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    a, b = l.split(':')
    R.append([int(a), [int(c) for c in b.split()]])


def check(s, v, cc,  cul, p):
    if p == len(v):
        return cul == s
    if cc:
        concat = int(str(cul)+str(v[p]))
        return check(s, v, cc, cul + v[p], p+1) or check(s, v, cc, cul*v[p], p+1) or check(s, v, cc, concat, p+1)
    else:
        return check(s, v, cc, cul + v[p], p+1) or check(s, v, cc, cul*v[p], p+1)


for s, v in R:
    if check(s, v, False, v[0], 1):
        T += s
    if check(s, v, True, v[0], 1):
        T2 += s

print(f"Tot {T} {T2}")
