#!/usr/bin/env pypy3

import fileinput
from collections import defaultdict
from functools import cmp_to_key

# counters
T = 0
T2 = 0

B = defaultdict(list)
A = defaultdict(list)
P = []
for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    if '|' in l:
        b, a = (int(c) for c in l.split('|'))

        B[b].append(a)
        A[a].append(b)
    elif ',' in l:
        P.append([int(c) for c in l.split(',')])


def is_ordered(pages):
    for i in range(len(pages)):
        for j in range(0, i):
            if pages[j] in B[pages[i]]:
                return False
            if pages[i] in A[pages[j]]:
                return False
        for j in range(i+1, len(pages)):
            if pages[j] in A[pages[i]]:
                return False
            if pages[i] in B[pages[j]]:
                return False
    return True


def compare(page1, page2):
    # page1 before page2
    if page2 in B[page1]:
        return -1
    if page1 in A[page2]:
        return -1

    # page2 before page1
    if page2 in A[page1]:
        return 1
    if page1 in B[page2]:
        return 1

    assert False, 'unsorted?'


for pages in P:
    if is_ordered(pages):
        T += pages[len(pages)//2]
    else:
        new_pages = sorted(pages, key=cmp_to_key(compare))
        T2 += new_pages[len(new_pages)//2]

print(f"Tot {T} {T2}")
