#!/usr/bin/env pypy3

import fileinput

# counters
T = 0
T2 = 0

R = dict()
P = list()
PC = 0
OUT = list()

for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    if l.startswith("Register"):
        reg, val = l.split(":")
        R[reg[-1:]] = int(val)
    if l.startswith("Program"):
        P = [int(c) for c in l[9:].split(',')]


SB = R['B']
SC = R['C']


stepsize = 1_000_000_000
#stepsize = 1_000
foundlen = False
foudddigits = 0
curdigit = len(P) - 1
i = 0
while True:
    PC = 0
    OUT = list()
    R['A'] = i
    R['B'] = SB
    R['C'] = SC

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

        # print(f'{opcode=} {operand=} {combo=}')

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
            break

    # find digit length
    if not foundlen and len(OUT) == len(P):
        i -= stepsize
        stepsize //= 10
        foundlen = True

    # find digits
    if foundlen and len(OUT) == len(P):
        if all(P[digit] == OUT[digit] for digit in range(curdigit, len(P))):
            i -= stepsize
            stepsize = max(stepsize//4, 1)
            curdigit -= 1
            if curdigit == -1:
                T2 = i+1
                break

    assert len(OUT) <= len(P), 'too far'
    i += stepsize


T = ",".join((str(c) for c in OUT))
print(f"Tot {T} {T2}")
