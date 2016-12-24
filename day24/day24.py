#!/usr/bin/env python3

from queue import Queue
from collections import namedtuple
from itertools import permutations



class Node:
  def __init__(self, x, y, name):
    self.x = x
    self.y = y
    self.name = name
    self.gscore = 0
    self.fscore = 0
    self.parent = None
  
  def dist_to(self, other):
    return abs(self.x - other.x) + abs(self.y - other.y)
  
  def neighbours(self, grid):
    pos = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    nh = []
    for p in pos:
      p = (self.x + p[0], self.y + p[1])
      if p[0] >= 0 and p[0] < len(grid[0]) and p[1] >= 0 and p[1] < len(grid):
        n = grid[p[1]][p[0]]
        #print('checking', n)
        if n.name != '#':
          nh.append(n)
          #print(' > OK')
        #else:
          #print(' > NOT OK')
        
    return nh
  
  def __repr__(self):
    return 'Node<%s>(x=%d, y=%d)' % (self.name, self.x, self.y)
  
  def __str__(self):
    return self.__repr__()
  
  def __eq__(self, other):
    """Override the default Equals behavior"""
    if other is not None and isinstance(other, self.__class__):
        return self.x == other.x and self.y == other.y
    return False
  
  def __hash__(self):
    return hash((self.x, self.y))


def clone(grid):
  gc = []
  for row in grid:
    rc = []
    for n in row:
      rc.append(Node(x=n.x, y=n.y, name=n.name))
    gc.append(rc)
  return gc

def find_sp_astar(grid, start, goal):
  start = grid[start.y][start.x]
  goal = grid[goal.y][goal.x]
  
  closed_set = set()
  open_set = {start}
  came_from = set()
  
  start.gscore = 0
  start.fscore = len(grid)*len(grid[0]) # max steps without going in circles
  
  while open_set:
    current = min(open_set, key=lambda n: n.gscore + n.fscore)
    if current == goal:
      break
      
    open_set.remove(current)
    closed_set.add(current)
    
    for n in current.neighbours(grid):
      if n in closed_set:
        continue
      t_gscore = current.gscore + n.dist_to(current)
      if n not in open_set:
        open_set.add(n)
      elif t_gscore >= n.gscore:
        continue # not a better path
      
      n.parent = current
      n.gscore = t_gscore
      n.fscore = n.gscore + n.dist_to(goal)
  
  if goal.parent:
    # reconstruct path
    path = []
    c = goal
    while c:
      path.append(c)
      c = c.parent
    return path
  return None
  




def load_grid(inpf):
  grid = []
  
  with open(inpf) as f:
    y = 0
    for line in f:
      line = line.strip()
      x = 0
      row = []
      for c in line:
        row.append(Node(x=x, y=y, name=c))
        x += 1
      y += 1
      grid.append(row)
   
  return grid

def find_markers(grid):
  markers = []
  for row in grid:
    for n in row:
      if n.name not in '.#':
        markers.append(n)
  return markers


def shortest_paths_all(grid, markers):
  # Find the shortest path between each node
  paths = {}
  for i in range(0, len(markers)):
    for j in range(0, len(markers)):
      if j != i:
        path = find_sp_astar(clone(grid), markers[i], markers[j])
        if not path:
          raise Exception('Failed to find path from %s to %s'%(markers[i], markers[j]))
        paths[markers[i].name + '-' + markers[j].name] = path
  return paths


def find_min_steps(markers, paths, p1=True):
  ms = [m.name for m in markers]
  lengths = {k: len(p)-1 for k,p in paths.items()}
  print(lengths)
  values = []
  print('Permutating of total %d markers'%len(markers))
  for perm in permutations(ms):
    if perm[0] != '0':
      continue
    length = 0
    for i in range(0, len(perm) - 1):
      ml = '%s-%s' % (perm[i], perm[i+1])
      length += lengths[ml]
    if not p1:
      ml = perm[-1] + '-0'
      length += lengths[ml]
    values.append((perm, length))
  return min(values, key=lambda l: l[1])

inf = 'input'
p1 = True

import sys

if 'test' in sys.argv:
  inf = 'test_input'
if 'p2' in sys.argv:
  p1 = False

grid = load_grid(inf)
markers = find_markers(grid)

print('Found %d markers.'% len(markers))
print('Loking up shortest paths between each.')
paths = shortest_paths_all(grid, markers)
print('Paths found. Trying all permutations to find the one with least distance')
perm, length = find_min_steps(markers, paths, p1)
print('Least steps (%d) on this track:'%length, perm)










