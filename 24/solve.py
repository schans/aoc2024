#!/usr/bin/env pypy3

import fileinput
from collections import defaultdict

# counters
T = 0
T2 = 0


gates = False
G = list()
R = dict()
GL = defaultdict(set)
i = 0
for line in fileinput.input():
    l = line.strip()
    if not l:
        gates = True
        continue

    if gates:
        ins, out = l.split(' -> ')
        p = ins.split()
        GL[p[0]].add(i)
        GL[p[2]].add(i)
        G.append({0: p[0], 1: p[2], 'op': p[1], 'out': out})
        i += 1
    else:
        p = l.split(': ')
        R[p[0]] = bool(int(p[1]))


def try_process(r, g):
    if g[0] in r and g[1] in r:
        match g['op']:
            case 'AND':
                r[g['out']] = r[g[0]] & r[g[1]]
            case 'XOR':
                r[g['out']] = r[g[0]] ^ r[g[1]]
            case 'OR':
                r[g['out']] = r[g[0]] | r[g[1]]
            case _:
                assert False, f"unknown operator {g['op']}"
        return True
    return False


def calc(r):
    p = set()
    c = len(r)
    while len(p) < len(G):
        for i, g in enumerate(G):
            if i in p:
                continue
            if try_process(r, g):
                p.add(i)
        if c == len(r):
            break
        c = len(r)
    s = 0
    for i in range(46):
        z = f"z{i:02d}"
        if z in r and r[z]:
            s += 1 << i
    return s


def get_reg(x, y):
    r = dict()  # reset regs
    # 44 bits
    for i in range(45):
        rx = f"x{i:02d}"
        ry = f"y{i:02d}"

        r[rx] = bool(x & (1 << i))
        r[ry] = bool(y & (1 << i))
    return r


def make_swap(i, j):
    oldi, oldj = G[i]['out'], G[j]['out']
    G[i]['out'] = oldj
    G[j]['out'] = oldi


def possible_swaps(x, y):
    swaps = set()
    for i in range(len(G)-1):
        for j in range(i+1, len(G)):
            make_swap(i, j)

            r = get_reg(x, y)
            z = calc(r)
            if x+y == z:
                swaps.add((i, j))

            # swap back
            make_swap(i, j)
    return swaps


def get_swapsets(x):
    swapsets = list()
    for j in range(45):
        y = 1 << j
        r = get_reg(x, y)
        z = calc(r)
        if x+y != z:
            swapsets.append(possible_swaps(x, y))
    return swapsets


def validate_swapset(swaps):
    assert len(swaps) == 4
    # swap
    for i in range(4):
        make_swap(*swaps[i])

    ones = 2**43 - 1
    for i in range(45):
        for j in range(45):
            x = ones ^ (1 << i)
            y = ones ^ (1 << j)
            r = get_reg(x, y)
            z = calc(r)
            if x+y != z:
                # swap back
                for i in range(4):
                    make_swap(*swaps[i])
                return False
    # swap
    for i in range(4):
        make_swap(*swaps[i])
    return True


def find_valid_swapset(swapsets):
    for sw1 in swapsets[0]:
        for sw2 in swapsets[1]:
            for sw3 in swapsets[2]:
                for sw4 in swapsets[3]:
                    if validate_swapset([sw1, sw2, sw3, sw4]):
                        # found solution
                        return [sw1, sw2, sw3, sw4]
    assert False, "no solution?"


T = calc(R)

swapsets = get_swapsets(0)
assert len(swapsets) == 4, "swaps not independant?"
swaps = find_valid_swapset(swapsets)

wires = set()
for sw in swaps:
    wires.add(G[sw[0]]['out'])
    wires.add(G[sw[1]]['out'])

T2 = ','.join(sorted(wires))
print(f"Tot {T} {T2}")
