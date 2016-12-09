#!/usr/bin/env python3

import re
import sys


inp_file = 'input'

if 'test' in sys.argv:
  inp_file = 'test-input'


decompressed = ''

def count_size(s):
  l = 0
  m = False
  for c in s:
    if c in ' \t\n\r':
      continue
    if c == '(' and not m:
      m = True
      continue
    if c == ')' and m:
      m = False
      continue
    if not m:
      l += 1
  return l

total = 0
gc = 0
with open(inp_file) as f:
  compressed = f.read()
  marker = ''
  i = 0
  while i < len(compressed):
    c = compressed[i]
    if c == '(' and not marker:
      if not marker:
        marker = '('
    elif c == ')' and marker:
      marker = marker[1:]
      marker = marker.split('x')
      cnt = int(marker[0])
      repeat = int(marker[1])
      chunk = compressed[i+1: i+cnt+1]
      chunk = ''.join([chunk for j in range(0, repeat)])
      compressed = chunk +compressed[i+1+cnt:]
      #print(' [c]>', chunk)
      #print(' [s]>', compressed)
      i = 0
      marker = ''
      #print(' [t]>', total)
      if gc % 1000 == 0:
        print(' >', len(compressed), ' [t]>', total)
      continue
    else:
      if not marker:
        if c not in ' \n\r\t':
          total += 1
      else:
        marker += c
    i += 1
    gc += 1

print (total)
