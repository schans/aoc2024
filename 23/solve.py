#!/usr/bin/env pypy3

import fileinput

# counters
T = 0
T2 = 0

L = list()
TS = set()
C = set()
for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    f, t = l.split('-')
    L.append({f, t})
    C.add((f, t))
    C.add((t, f))
    if f.startswith('t'):
        TS.add(f)
    if t.startswith('t'):
        TS.add(t)


def is_full_connected(conn, l):
    f, t = l

    if not f in conn and not t in conn:
        return False

    if f in conn and t in conn:
        return False

    d = (l ^ conn).pop()
    for c in conn:
        if (d, c) not in C:
            return False

    return True


seen = set()
for conn in L:
    for l in L:
        if is_full_connected(conn, l):
            n = frozenset(conn | l)
            s = ",".join(sorted(n))
            if n not in seen:
                seen.add(n)
                if n & TS:
                    T += 1

while True:
    ns = set()
    for conn in seen:
        for l in L:
            if is_full_connected(conn, l):
                n = frozenset(conn | l)
                if n not in ns:
                    ns.add(n)
    if len(ns) == 0:
        break
    seen = ns

T2 = ",".join(sorted(seen.pop()))
print(f"Tot {T} {T2}")
