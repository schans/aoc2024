#!/usr/bin/env pypy3

import fileinput
from functools import cmp_to_key


# counters
T = 0
T2 = 0


B = {}
A = {}
O = []
for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    if '|' in l:
        b, a = (int(c) for c in l.split('|'))

        if b in B:
            B[b].append(a)
        else:
            B[b] = [a]
        if a in A:
            A[a].append(b)
        else:
            A[a] = [b]
    elif ',' in l:
        O.append([int(c) for c in l.split(',')])


def is_correct(order):
    for i in range(len(order)):
        for j in range(0, i):
            if order[i] in B and order[j] in B[order[i]]:
                return False
            if order[j] in A and order[i] in A[order[j]]:
                return False
        for j in range(i+1, len(order)):
            if order[i] in A and order[j] in A[order[i]]:
                return False
            if order[j] in B and order[i] in B[order[j]]:
                return False
    return True


def compare(item1, item2):
    # item1 before item2
    if item1 in B and item2 in B[item1]:
        return -1
    if item2 in A and item1 in A[item2]:
        return -1

    # item2 before item1
    if item1 in A and item2 in A[item1]:
        return 1
    if item2 in B and item1 in B[item2]:
        return 1

    assert False, 'unsorted?'


def sort_order(order):
    if is_correct(order):
        return order
    new_order = sorted(order, key=cmp_to_key(compare))
    return sort_order(new_order)


for order in O:
    if is_correct(order):
        T += order[len(order)//2]
    else:
        new_order = sort_order(order)
        T2 += new_order[len(new_order)//2]

print(f"Tot {T} {T2}")
