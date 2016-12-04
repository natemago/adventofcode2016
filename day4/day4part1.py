#!/usr/bin/env python3

import re
from functools import reduce
import sys

def is_real_room(room_name, checksum):
  letters = {}
  for l in room_name:
    if l =='-':
      continue
    if not letters.get(l):
      letters[l] = 0
    letters[l] += 1
  letters = [(l, count) for l, count in letters.items()]
  
  letters = sorted(sorted(letters, key=lambda i: i[0]), key=lambda i: i[1], reverse=True)
  calc_checksum = reduce(lambda a, i: a+i[0], letters[0:5], '')
  return calc_checksum == checksum

if 'test' in sys.argv:
  print(is_real_room('aaaaa-bbb-z-y-x', 'abxyz'))
  
  sys.exit(0)




sector_sum = 0

with open('input') as f:
  for line in f:
    line = line.strip()
    m = re.match('(?P<room>[\w-]+)-(?P<sector_id>\d+)\[(?P<checksum>\w+)\]', line)
    if not m:
      raise Exception('Oops: ' + line)
    room_name = m.group('room')
    sector_id = int(m.group('sector_id'))
    checksum = m.group('checksum')
    
    if is_real_room(room_name, checksum):
      sector_sum += sector_id

print(sector_sum)