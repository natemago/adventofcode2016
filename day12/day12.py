#!/usr/bin/env python3

import re
import sys

REGS = {'a': 0,'b': 0, 'c': 0, 'd': 0}
MEM = []
PC = 0

if 'p2' in sys.argv:
  REGS['c'] = 1

with open('input') as f:
  for line in f:
    line = line.strip()
    MEM.append(line)

while(True):
  if PC < 0 or PC >= len(MEM):
    break
  line = MEM[PC].split(' ')
  #print(line, REGS)
  if line[0] == 'cpy':
    x = line[1]
    y = line[2]
    if x.isalpha():
      REGS[y] = REGS[x]
    else:
      REGS[y] = int(x)
  elif line[0] == 'inc':
    REGS[line[1]] += 1
  elif line[0] == 'dec':
    REGS[line[1]] -= 1
  else:
    x = line[1]
    y = line[2]
    if y.isalpha():
      y = REGS[y]
    else:
      y = int(y)
    if x.isalpha():
      if REGS[x]:
        PC += y
        continue
    else:
      if int(x):
        PC += y
        continue
  PC += 1  
print(REGS) 