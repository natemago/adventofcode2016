#!/usr/bin/env python3

from hashlib import md5
from queue import Queue
from collections import namedtuple


salt = 'hhhxzeay'

dirs = { 'U': 0, 'D': 1, 'L': 2, 'R': 3 }


def allowed_paths(x, y, path, salt):
  hsh = md5((salt+path).encode('utf-8')).hexdigest()[0:4]
  all_paths = [(x-1, y, 'L'), (x+1, y, 'R'), (x, y-1, 'U'), (x, y+1, 'D')]
  all_paths = filter(lambda p: p[0] >= 0 and p[0] < 4 and p[1] >= 0 and p[1] < 4, all_paths)
  
  paths = []
  key = 'bcdef'
  for x,y,d in all_paths:
    if hsh[dirs[d]] in 'bcdef':
      paths.append((x,y,d))
  return paths
  
"""
BFS to reach the shortest paths first.
"""
  
Move = namedtuple('Move', ['x','y','path', 'steps'])

visited = {}

q = Queue()

q.put(Move(x=0, y=0, path='', steps=0))

solution = None

while not q.empty():
  move = q.get()
  if move.x == 3 and move.y == 3:
    if solution is None or move.steps < solution.steps:
      solution = move
  if solution and solution.steps < (move.steps+ 1):
    continue

  for x, y, d in allowed_paths(move.x, move.y, move.path, salt):
    q.put(Move(x=x, y=y, path=move.path+d, steps=move.steps+1))


print('Solution: ', solution)