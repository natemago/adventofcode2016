#!/usr/bin/env python3

import re
import sys




if 'test' in sys.argv:
  print('Test')
  sys.exit(0)


decompressed = ''

def count_size(s):
  l = 0
  for c in s:
    if c in ' \t\n\r':
      continue
    l += 1
  return l

total = 0
with open('input') as f:
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
      compressed = ''.join([chunk for j in range(0, repeat)]) +compressed[i+1+cnt:]
      i = 0
      marker = ''
      total += count_size(chunk)
      print(' >', len(compressed))
      continue
    else:
      if not marker:
        if c not in ' \n\r\t':
          total += 1
      else:
        marker += c
    i += 1

print (total)
