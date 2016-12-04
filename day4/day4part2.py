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

def decypher_room_name(room_name, sector_id):
  decyphered = ''
  for c in room_name:
    if c == '-':
      decyphered += ' '
    else:
      o = ord(c) - ord('a')
      c = chr((o + sector_id)%26 + ord('a'))
      decyphered += c
  return decyphered

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
      real_name = decypher_room_name(room_name, sector_id)
      # print the rooms and grep for 'north'
      if 'print_names'in sys.argv:
        print(real_name)
      else:
        if real_name == 'northpole object storage':
          print(sector_id)
