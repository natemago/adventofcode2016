#!/usr/bin/env python3

import re
from math import ceil

def swap_pos(s, x, y):
  sa = [c for c in s]
  t = sa[x]
  sa[x] = sa[y]
  sa[y] = t
  return ''.join(sa)

def swap_letter(s, x, y):
  return s.replace(x, '*').replace(y, x).replace('*', y)

def rotate(s, direction, x):
  x = x%len(s)
  if direction == 'left':
    return s[x:] + s[0:x]
  elif direction == 'right':
    return s[-x:] + s[0:-x]

def rotate_on_pos(s, x):
  if not x in s:
    return s
  i = s.index(x)
  if i >= 4:
    i += 1
  i += 1
  print(' >>> r: letter ', x, i, 'positions. Orig pos: ', s.index(x))
  return rotate(s, 'right', i)

def reverse(s, x, y):
  rev = ''.join(reversed(s[x:y+1]))
  return s[0:x] + rev + s[y+1:]

def move(s, x, y):
  t = s[x]
  s = s[0:x] + s[x+1:]
  return s[0:y] + t + s[y:]


def est_orig_pos(cpos, lens):
  i = 0
  while True:
    p = i*2
    if i >= 4:
      p+=2
    else:
      p+=1
    if p%lens == cpos:
      return i
    i += 1


def inv_rotate_pos(s, x):
  t = s.index(x)
  o = est_orig_pos(t, len(s))
  shift = o+1
  if o >= 4:
    shift+=1
  print('  >>> unrotate letter', x, '. Orig pos:', o, 'Unrotating:', shift)
  return rotate(s, 'left', shift)
  
  
operations = {
  'swap position (\d+) with position (\d+)': lambda s, m: swap_pos(s, int(m.group(1)), int(m.group(2))),
  'swap letter (\w) with letter (\w)': lambda s, m: swap_letter(s, m.group(1), m.group(2)),
  'rotate (\w+) (\d+) steps{0,1}': lambda s, m: rotate(s, m.group(1), int(m.group(2)) ),
  'rotate based on position of letter (\w)': lambda s, m: rotate_on_pos(s, m.group(1)),
  'reverse positions (\d+) through (\d+)': lambda s, m: reverse(s, int(m.group(1)), int(m.group(2))),
  'move position (\d+) to position (\d+)': lambda s, m: move(s, int(m.group(1)), int(m.group(2)))
}

unscramble_operations = {
  'swap position (\d+) with position (\d+)': lambda s, m: swap_pos(s, int(m.group(1)), int(m.group(2))),
  'swap letter (\w) with letter (\w)': lambda s, m: swap_letter(s, m.group(1), m.group(2)),
  'rotate (\w+) (\d+) steps{0,1}': lambda s, m: rotate(s, 'left' if m.group(1) == 'right' else 'right', int(m.group(2)) ),
  'rotate based on position of letter (\w)': lambda s, m: inv_rotate_pos(s, m.group(1)),
  'reverse positions (\d+) through (\d+)': lambda s, m: reverse(s, int(m.group(1)), int(m.group(2))),
  'move position (\d+) to position (\d+)': lambda s, m: move(s, int(m.group(2)), int(m.group(1)))
}


def load_instrs(instf):
  instrs = []
  with open(instf) as f:
    for line in f:
      instrs.append(line.strip())
  return instrs

def scramble(password, instrs, operations):
  for instr in instrs:
    executed = False
    print('insr ->', instr, '[', password, ']')
    for expression, operation in operations.items():
      m = re.match(expression, instr)
      if m:
        password = operation(password, m)
        executed = True
        print(' >>', password)
        break
    if not executed:
      raise Exception('Failed to match: ' + line)
  return password


def unscramble(password, instrs, operations):
  instrs = reversed(instrs)
  return scramble(password, instrs, operations)


import sys

inp = 'abcdefgh'
instr = 'input'

if 'test' in sys.argv:
  inp = 'abcde'
  instr = 'test_input'
  
p1pass = scramble(inp, load_instrs(instr), operations)
print('Part1: ', p1pass)
print('----------------------')
print('Part2: ', unscramble('fbgdceah', load_instrs(instr), unscramble_operations))





