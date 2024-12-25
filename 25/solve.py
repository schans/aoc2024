#!/usr/bin/env pypy3

import fileinput
from collections import defaultdict
from typing import List

# counters
T = 0

L = list()
K = list()
LL = LH = 0


def parse(ss: List[str]):
    m = defaultdict(int)
    for s in ss:
        for i, c in enumerate(s):
            if c == '#':
                m[i] += 1
    if ss[0][0] == '.':
        K.append(m)
    else:
        L.append(m)


s = list()
for line in fileinput.input():
    l = line.strip()
    if not l:
        parse(s)
        LL = len(s[0])
        LH = len(s)
        s = list()
        continue
    s.append(l)
# last
parse(s)

for l in L:
    for k in K:
        T += all(k[i] + l[i] <= LH for i in range(LL))

print(f"Tot {T}")
