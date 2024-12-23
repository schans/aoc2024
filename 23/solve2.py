#!/usr/bin/env pypy3

import fileinput
from collections import defaultdict

# counters
T = 0
T2 = 0

G = defaultdict(set)
for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    f, t = l.split('-')
    G[f].add(t)
    G[t].add(f)


def get_full_connected(n, conn):
    k = frozenset(conn)
    if k in connected:
        return
    connected.add(k)

    for nn in G[n]:
        if nn in conn:
            continue
        if all(nn in G[c] for c in conn):
            get_full_connected(nn, {*conn, nn})


triples = set()
for k in G:
    for l in G[k]:
        if k == l:
            continue
        for m in G[l]:
            if m not in G[k]:
                continue
            triples.add(frozenset({k, l, m}))
T = len([t for t in triples if any(n.startswith("t") for n in t)])

connected = set()
for k in G:
    get_full_connected(k, {k})
maxs = max(connected, key=len)
T2 = ",".join(sorted(max(connected, key=len)))

print(f"Tot {T} {T2}")
