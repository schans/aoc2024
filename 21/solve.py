#!/usr/bin/env pypy3

import fileinput
from functools import cache
from heapq import heapify, heappop, heappush

# counters
T = 0
T2 = 0

DIRS = ((0, 1), (0, -1), (-1, 0), (1, 0))
RDIRS = {(0, 1): '>',  (0, -1): '<',  (-1, 0): '^', (1, 0): 'v'}
'''
numpad
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+

dirpad
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
'''
PADS = {
    'numpad': {
        '7': (0, 0),
        '8': (0, 1),
        '9': (0, 2),
        '4': (1, 0),
        '5': (1, 1),
        '6': (1, 2),
        '1': (2, 0),
        '2': (2, 1),
        '3': (2, 2),
        '0': (3, 1),
        'A': (3, 2),
    },
    'dirpad': {
        '^': (0, 1),
        'A': (0, 2),
        '<': (1, 0),
        'v': (1, 1),
        '>': (1, 2),
    }
}

R = []
for line in fileinput.input():
    l = line.strip()
    if not l:
        continue
    R.append(l)


@cache
def presses_to_next_key(ptype, fr, to):
    pad = PADS[ptype]
    rpad = dict()
    for k, v in pad.items():
        rpad[v] = k

    presses = list()
    shortest = 10**6
    seen = dict()
    pq = list()
    pq.append((0, pad[fr], list()))
    heapify(pq)
    while pq:
        d, (r, c), p = heappop(pq)
        if d > shortest:
            continue

        if (r, c) == pad[to]:
            shortest = d
            presses.append("".join(p) + 'A')

        if (r, c) in seen:
            if d > seen[(r, c)]:
                continue
        seen[(r, c)] = d

        for (dr, dc) in DIRS:
            rr, cc = r+dr, c+dc
            if (rr, cc) in rpad:
                pp = [*p, RDIRS[(dr, dc)]]
                heappush(pq, (d+1, (rr, cc), pp))
    return presses


@cache
def get_key_presses(np, r):
    sols = list()
    sols.append("")
    fr = 'A'
    for c in r:
        to = c
        press = presses_to_next_key(np, fr, to)
        if len(press) == 1:
            for k, v in enumerate(sols):
                sols[k] = v + press[0]
        else:
            new_sols = list()
            for pr in press:
                for k, v in enumerate(sols):
                    new_sols.append(v + pr)
            sols = new_sols
        fr = to
    return sols


@cache
def get_key_count(presses, d):
    if d == 0:
        return len(presses)

    # expand to next layer
    mcnt = 10**16
    expands = get_key_presses('dirpad', presses)
    for new_presses in expands:
        cnt = 0
        parts = new_presses.split('A')
        for pp in parts:
            if pp == "":
                cnt += 1
            else:
                cnt += get_key_count(pp+'A', d-1)
        mcnt = min(mcnt, cnt)
    return mcnt - 1


def get_min_key_count(presses, layers):
    cnt = 10**16
    for pr in presses:
        cnt = min(cnt, get_key_count(pr, layers))
    return cnt


for r in R:
    presses = get_key_presses('numpad', r)
    T += get_min_key_count(presses, 2) * int(r[:-1])
    T2 += get_min_key_count(presses, 25) * int(r[:-1])

print(f"Tot {T} {T2}")
