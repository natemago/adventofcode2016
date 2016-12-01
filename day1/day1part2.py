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
  visited = []
  rot = ROTS[D]
  direction = p['dir']
  position = p['pos']
  direction = rot(direction)
  
  for i in range(0, x):
    position = add(position, direction)
    visited.append(position)
    
  p['pos'] = position
  p['dir'] = direction
  return p, visited




P = { 'pos': [0,0], 'dir': [1,0] }
visited = {'0:0'}

with open('input-p1') as f:
  cnt = f.read()
  instrs = cnt.split(',')
  for inst in instrs:
    inst = inst.strip()
    rot = inst[0].upper()
    x = int(inst[1:])
    P, vs = move(P, rot, x)
    ebh_found = False
    for v in vs:
      k = '%d:%d' % (v[0],v[1])
      if k in visited:
        ebh_found = True
        P['pos'] = v
        break
      visited.add(k)
    if ebh_found:
      break

print('First position visited twice:', P['pos'])
print('Distance: ', abs(P['pos'][0]) + abs(P['pos'][1]))
