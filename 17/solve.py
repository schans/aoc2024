#!/usr/bin/env pypy3

import fileinput
from re import findall

# counters
T = 0
T2 = 0

R = dict()
P = list()
PC = 0
OUT = list()


def ints(s):
    return list(map(int, findall(r'\d+', s)))


for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    if l.startswith("Register"):
        reg, val = l.split(":")
        R[reg[-1:]] = int(val)
    if l.startswith("Program"):
        P = ints(l)

while True:
    opcode = P[PC]
    operand = P[PC+1]

    combo = -1
    if 0 <= operand < 4:
        combo = operand
    elif operand == 4:
        combo = R['A']
    elif operand == 5:
        combo = R['B']
    elif operand == 6:
        combo = R['C']
    elif operand == 7:
        assert False, "reserved"

    if opcode == 0:
        # adv
        R['A'] = R['A'] // 2**combo
    elif opcode == 1:
        # bxl
        R['B'] = R['B'] ^ operand
    elif opcode == 2:
        # bst
        R['B'] = combo % 8
    elif opcode == 3:
        # jnz
        if R['A'] != 0:
            PC = operand - 2  # compensate for increase
    elif opcode == 4:
        # bxc
        R['B'] = R['B'] ^ R['C']
    elif opcode == 5:
        # out
        OUT.append(combo % 8)
    elif opcode == 6:
        # bdv
        R['B'] = R['A'] // 2**combo
    elif opcode == 7:
        # cdv
        R['C'] = R['A'] // 2**combo
    else:
        assert False, ('unknown opcode', opcode)

    # increment
    PC += 2
    if PC >= len(P):
        # end of program
        break

T = ",".join((str(c) for c in OUT))

# Reverse engineer for input: 2,4, 1,5, 7,5, 1,6, 0,3, 4,0, 5,5, 3,0
# bst:  b = a % 8
# bxl:  b = b ^ 5
# cdv:  c = a >> b
# bxl:  b = b ^ 6
# adv:  a = a >> 3
# bxc:  b = b ^ c
# out:  out(b % 8)


def solve_from_back(p, cur):
    if len(p) == 0:
        return cur

    for k in range(8):
        a = cur << 3 | k
        b = a % 8
        b = b ^ 5
        c = a >> b
        b = b ^ 6
        b = b ^ c
        out = b % 8
        if out == p[-1]:
            nout = solve_from_back(p[:-1], a)
            if nout == None:
                continue
            else:
                return nout


T2 = solve_from_back(P, 0)

print(f"Tot {T} {T2}")
