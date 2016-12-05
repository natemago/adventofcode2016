#!/usr/bin/env python3

from hashlib import md5


INPUT = 'uqwqemis'

def passchars(seed, cn):
  seq = 0
  count = 0
  while True:
    if count == cn:
      break
    hsh = md5( (seed + str(seq)).encode('utf-8') ).hexdigest()
    #print(seq, ')', hsh)
    if seq % 1000000 == 0:
      print(seq)
    if hsh[0:5] == '00000':
      count += 1
      yield hsh[5]
    seq += 1
    
    
import sys
if 'test' in sys.argv:
  print('|'.join([c for c in passchars('abc', 8)]))
else:
  print(''.join([c for c in passchars(INPUT, 8)]))
