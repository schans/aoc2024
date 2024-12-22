#!/usr/bin/env pypy3

import fileinput

# counters
T = 0
T2 = 0

S = list()

for line in fileinput.input():
    l = line.strip()
    if not l:
        continue
    S.append(int(l))


def get_secret(s, n):
    seq = list()
    seq.append(s % 10)
    for _ in range(n):
        s = (s ^ (s << 6)) % 16777216
        s = (s ^ (s >> 5)) % 16777216
        s = (s ^ (s << 11)) % 16777216
        seq.append(s % 10)
    return s, seq


SQ = list()
SQH = list()
UH = set()


def gen_map(seq, n):
    p = list()
    p.append(seq[0])
    p.append(seq[1])
    p.append(seq[2])
    p.append(seq[3])
    p.append(seq[4])

    sh = dict()
    for i in range(5, n):
        d = list()
        for v1, v2 in list(zip(p, p[1:])):
            d.append(v2 - v1)
        tup = tuple(d)
        # only first seq
        if tup not in sh:
            sh[tup] = seq[i-1]
        UH.add(tup)
        p.pop(0)
        p.append(seq[i])
    SQH.append(sh)


for s in S:
    t, seq = get_secret(s, 2000)
    T += t
    SQ.append(seq)
    gen_map(seq, 2000)

for tup in UH:
    t = 0
    for i in range(len(S)):
        if tup in SQH[i]:
            t += SQH[i][tup]
    T2 = max(T2, t)

print(f"Tot {T} {T2}")
