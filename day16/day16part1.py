#!/usr/bin/env python3

data = '01110110101001000'
disk_length = 272

import sys

if 'p2' in sys.argv:
  disk_length = 35651584


checksum = data

def tr(s, o, t):
  translated = ''
  d = {o[i]:t[i] for i in range(0, len(o))}
  for c in s:
    if c in o:
      translated += d[c]
    else:
      translated += c
  return translated

while len(checksum) < disk_length:
  checksum = checksum + '0' + tr(''.join(reversed(checksum)),'10','01')

checksum = checksum[0:disk_length]

while len(checksum)%2 == 0:
  n = 0
  c = ''
  while n < len(checksum):
    c += '1' if checksum[n] == checksum[n+1] else '0'
    n += 2
  checksum = c
print(checksum)