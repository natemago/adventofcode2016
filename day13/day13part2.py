#!/usr/bin/env python3

import sys
import queue
import collections

"""
0000 - 0
0001 - 1
0010 - 1
0011 - 0
0100 - 1
0101 - 0
0110 - 0
0111 - 1

1000 - 1
1001 - 0
1010 - 0
1011 - 1
1100 - 0
1101 - 1
1110 - 1
1111 - 0
"""

t1 = [0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0]
T = []
MAX_BYTES = 4
MAX_SIZE = 2**(MAX_BYTES*8) - 1

for i in range(0, 16):
  for j in range(0, 16):
    T.append((t1[i] + t1[j])%2)

def is_odd(n):
  if n > MAX_SIZE:
    raise Exception('Beyond %d bytes: ' % (MAX_BYTES, n))
  c = 0
  mask = 0xFF
  for i in range(0, MAX_BYTES):
    c = (c<<1) | T[n&mask]
    n = n >> 8
  return T[c]

def is_open_space(x, y, magic):
  return is_odd(x*x + 3*x + 2*x*y + y + y*y + magic) == 0

def get_pos(x,y):
  pos = [(x+1, y), (x, y+1)]
  if x > 0:
    pos.append((x-1, y))
  if y > 0:
    pos.append((x, y-1))
  return pos


for i in range(0, 10):
  for j in range(0, 10):
    print('#' if is_open_space(j, i, 10) else '.', end='')
  print('')





Entry = collections.namedtuple('Entry', ['x','y','prev','steps'])

BREAK_ON_FIRST = False
MAGIC = 1352

visited = {(1,1)}

q = queue.Queue()

count = 0

q.put(Entry(x=1, y=1, prev=(1,1), steps=0))
  
while not q.empty():
  e = q.get()
  visited.add((e.x,e.y))
  count += 1
  if e.steps == 50:
    continue
  for x,y in get_pos(e.x, e.y):
    if is_open_space(x,y, MAGIC) and not (x,y) in visited:
      q.put(Entry(x=x, y=y, prev=(e.x, e.y), steps=e.steps + 1))
      
print(len(visited))
for i in range(0, 40):
  for j in range(0, 40):
    if j == 31 and i == 39:
      print('X', end='')
    #elif (j,i) in visited:
    #  print('o', end='')
    else:
      print('.' if is_open_space(j, i, 1352) else '#', end='')
  print('')

