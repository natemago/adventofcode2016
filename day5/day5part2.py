#!/usr/bin/env python3

from hashlib import md5
from random import randint

INPUT = 'uqwqemis'

def hack_password(seed, cn):
  seq = 0
  count = 0
  password = ['*' for i in range(0, cn)]
  while True:
    hsh = md5( (seed + str(seq)).encode('utf-8') ).hexdigest()
    if hsh[0:5] == '00000':
      pos = int(hsh[5], 16)
      if pos >= 0 and pos < cn and password[pos] == '*':
        c = hsh[6]
        password[pos] = c
        count += 1
    seq += 1
    if seq % 100 == 0:
      cinematic_preview(password)
    if not ('*' in password):
      break
  cinematic_preview(password)
  print('\nF O U N D')
    
def cinematic_preview(password):
  s = ''
  for c in password:
    if c == '*':
      s += str(randint(0,9))
    else:
      s += '\x1b[31m%s\x1b[0m' % c
  s = '[%s]' % s
  b = ''.join(['\b' for i in range(0, len(s)+2)])
  print(s,b,end='')

import sys
if 'test' in sys.argv:
  hack_password('abc', 8)
else:
  hack_password(INPUT, 8)
