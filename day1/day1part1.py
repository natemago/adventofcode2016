#!/usr/bin/env python3

def L(v):
  "90 deg rotation"
  return [-v[1],v[0]]

def R(v):
  "270 deg rotation"
  return [v[1], -v[0]]

ROTS = {'R': R, 'L': L}


def add(v1, v2):
  return [v1[0] + v2[0], v1[1] + v2[1]]

def move(p, D, x):
  rot = ROTS[D]
  direction = p['dir']
  position = p['pos']
  direction = rot(direction)
  p['pos'] = add(position, [x*direction[0], x*direction[1]])
  p['dir'] = direction
  return p




P = { 'pos': [0,0], 'dir': [1,0] }

with open('input-p1') as f:
  cnt = f.read()
  instrs = cnt.split(',')
  for inst in instrs:
    inst = inst.strip()
    rot = inst[0].upper()
    x = int(inst[1:])
    P = move(P, rot, x)

print('Final position:', P['pos'])
print('Distance: ', abs(P['pos'][0]) + abs(P['pos'][1]))
