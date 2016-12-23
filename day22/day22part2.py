#!/usr/bin/env python3

import re
from collections import namedtuple
from queue import Queue

Pos  = namedtuple('Pos', ['x','y'])


class Node:
  def __init__(self, x, y, size, used, avail, use):
    self.gscore = 0
    self.fscore = 0
    self.x = x
    self.y = y
    self.size = size
    self.used = used
    self.avail = avail
    self.use = use
    self.parent = None
  
  def neighbours(self, grid, cv):
    return[grid[p.y][p.x] for p in allowed_pos(grid, Pos(self.x, self.y), cv)]
  
  def dist_to(self, other):
    return abs(self.x - other.x) + abs(self.y - other.y)
  
  def __repr__(self):
    return 'N(x=%d, y=%d, used=%d, avail=%d)' % (self.x, self.y, self.used, self.avail)
  
  def __str__(self):
    return self.__repr__()

def load_nodes(inpf):
  nodes = []
  with open(inpf) as f:
    for line in f:
      line = line.strip()
      if line.startswith('/dev'):
        m = re.search('/dev/grid/node-x(?P<x>\d+)-y(?P<y>\d+)\s+(?P<size>\d+)T\s+(?P<used>\d+)T\s+(?P<avail>\d+)T\s+(?P<use>\d+)%', line)
        x = int(m.group('x'))
        y = int(m.group('y'))
        size = int(m.group('size'))
        used = int(m.group('used'))
        avail = int(m.group('avail'))
        use = int(m.group('use'))
        
        nodes.append(Node(x=x, y=y, size=size, used=used, avail=avail, use=use))
  return nodes
 
def get_grid(nodes):
  gsx = max(nodes, key=lambda n: n.x).x + 1
  gsy = max(nodes, key=lambda n: n.y).y + 1

  grid = [[None for i in range(0, gsx)] for j in range(0, gsy)]
  for n in nodes:
    grid[n.y][n.x] = n
  
  return grid


nodes = load_nodes('input')
grid = get_grid(nodes)
target = grid[0][-1]

def allowed_pos(grid, pos, cv):
  ps = []
  for p in [(0,-1), (-1, 0), (1, 0), (0, 1)]:
    p = (pos.x+p[0],pos.y+p[1])
    if p[0] >= 0 and p[0] < len(grid[0]) and p[1] >= 0 and p[1] < len(grid) and grid[p[1]][p[0]].used <= cv:
      ps.append(Pos(x=p[0],y=p[1]))
  
  return ps


def as_str(grid, path=None, avail=None):
  s = ''
  for row in grid:
    for n in row:
      p = Pos(x=n.x, y=n.y)
      if path and n in path:
        if avail and n.used > avail:
          s += 'O'
        else:
          s += '*'
      else:
        if avail and n.used > avail:
          s += 'X'
        else:
          s += '.'
    s += '\n'
  return s
  

def a_star(start, goal, grid, cv):
  closed_set = set()
  open_set = {start}
  came_from = set()
  
  start.gscore = 0
  start.fscore = len(grid)*len(grid[0]) # max steps without going in circles
  
  while open_set:
    current = min(open_set, key=lambda n: n.gscore + n.fscore)
    if current == goal:
      print('Found')
      break
      # found it, but keep on going for a better path
    open_set.remove(current)
    closed_set.add(current)
    
    for n in current.neighbours(grid, cv):
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


# Check some stuff out

# find the biggest hole
max_hole = max(nodes, key=lambda n: n.avail)
print(max_hole)

# is the hole bigger than all in the first row
bigger = True
for r in [0,1]:
  for n in grid[r]:
    if n.used > max_hole.avail:
      bigger = False
      break
print('Is the hole bigger than all in rows 0 and 1:', bigger)
if not bigger:
  raise Exception('Cannot go with trivial solution!')

print('It seems that it is. We can shift the data around if we manage to bring the hole in front of the target node.')
# Trivial solution

path = a_star(max_hole, grid[0][-2], grid, max_hole.avail)
print('Path found - ', path)
print('Path length:', len(path))
print(as_str(grid, path=path, avail=max_hole.avail))

print('Min Steps Needed: ', len(path)-1 + 5*(len(grid[0]) - 2) + 1) 

