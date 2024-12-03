#!/usr/bin/env pypy3

import fileinput
import re
# counters
T = 0
T2 = 0


enabled = True
for line in fileinput.input():
    l = line.strip()
    if not l:
        continue

    for match in re.finditer('do\(\)|don\'t\(\)|mul\(\d{1,3},\d{1,3}\)', l):
        mtch = match.group()
        if mtch == 'do()':
            enabled = True
        elif mtch == 'don\'t()':
            enabled = False
        else:
            nums = [int(c) for c in mtch[4:-1].split(',')]
            T += nums[0] * nums[1]
            if enabled:
                T2 += nums[0] * nums[1]

print(f"Tot {T} {T2}")
