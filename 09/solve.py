#!/usr/bin/env pypy3

import fileinput

# counters
T = 0
T2 = 0

L = list()
F = list()
FS, FL = list(), list()
ES, EL = list(), list()

for line in fileinput.input():
    l = line.strip()
    if not l:
        continue
    L = [*map(int, l)]


cur = 0
for i in range(0, len(L), 2):
    v = i//2
    FS.append(cur)
    FL.append(L[i])
    for _ in range(L[i]):
        F.append(v)
    if i+1 < len(L):
        ES.append(cur+L[i])
        EL.append(L[i+1])
        cur += (L[i] + L[i+1])


cur = 0
while F:
    if F[0] == 0:
        T += cur * F.pop(0)
        cur += 1
        continue

    for _ in range(EL[F[0]-1]):
        if len(F):
            T += cur * F.pop()
            cur += 1

    while len(F) > 1 and F[0] == F[1]:
        T += cur * F.pop(0)
        cur += 1

    if len(F):
        T += cur * F.pop(0)
        cur += 1


for f in range(len(FS)-1, -1, -1):
    for e in range(len(ES)):
        fs, fl = FS[f], FL[f]
        es, el = ES[e], EL[e]
        if es >= fs:
            # don't move back
            break
        if el >= fl:
            # move
            FS[f] = es
            ES[e] += fl
            EL[e] -= fl
            break


for f in range(len(FS)):
    for i in range(FL[f]):
        cur = FS[f] + i
        T2 += cur * f

print(f"Tot {T} {T2}")
