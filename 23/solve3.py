#!/usr/bin/env python3

import fileinput
from collections import defaultdict
import networkx as nx


# counters
T = 0
T2 = 0

G = nx.Graph()
for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    f, t = l.split('-')
    G.add_edge(f, t)

for n in G:
    for fn in G[n]:
        for sn in G[fn]:
            if sn in G[n] and any(s.startswith('t') for s in [n, fn, sn]):
                T += 1
T //= 6
T2 = ",".join(sorted(max(nx.find_cliques(G), key=len)))

print(f"Tot {T} {T2}")
