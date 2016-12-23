#!/usr/bin/env python3

import re
from collections import namedtuple

Node = namedtuple('Node', ['x','y','size','used','avail','use'])

nodes = []
seen = set()
with open('input') as f:
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
      
      n = (x,y)
      if n in seen:
        print('seen', n)
      seen.add(n)
      
      nodes.append(Node(x=x, y=y, size=size, used=used, avail=avail, use=use))
      if used+avail != size:
        print(x,y,size,used,avail,use)
      if used == 0 or use == 100:
        print(nodes[-1])
      
"""
for n in nodes:
  print(n)
"""

print('total:',len([i for i in filter(lambda n: n.used > 0 and n.used <= 90, nodes)]))

count = 0
checked =0
for a in nodes:
  for b in nodes:
    if a.x != b.x or a.y != b.y:
      if a.used and a.used <= b.avail:
        #print(a,b)
        count+=1

      
print(nodes[0])
print(len(nodes))
print(count)
print(checked)
"""
for u in unviable:
  print(u)
"""