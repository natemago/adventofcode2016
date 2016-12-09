#!/usr/bin/env python3

import re
import sys




if 'test' in sys.argv:
  print('Test')
  sys.exit(0)


decompressed = ''

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
      decompressed += ''.join([chunk for j in range(0, repeat)])
      i += cnt + 1
      marker = ''
      continue
    else:
      if not marker:
        decompressed += c
      else:
        marker += c
    i += 1

l = 0
for c in decompressed:
  if c in ' \t\n\r':
    continue
  l += 1
print(l)
