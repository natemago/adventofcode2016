#!/usr/bin/env python3

import re

count = 0

with open('input') as f:
  for line in f:
    line = line.strip()
    found = False
    for part in re.sub(r'\[(\w+)\]','|',line).split('|'):
      for i in range(0, len(part)-2):
        aba = part[i: i+3]
        if aba[0] != aba[2] or aba[0] == aba[1]:
          continue
        bab = aba[1] + aba[0] + aba[1]
        for m2 in re.finditer(r'\[(\w+)\]', line):
          hyper = m2.group(1)
          if bab in hyper:
              found = True
              break
      if found:
        break
    if found:
      count += 1
      
print(count)
