#!/usr/bin/env python3

"""
If we drop the ball at time t, the disk d will be at position:
 
X = t+s+d

where d is the disknumber and s is the startig pos.


"""
# startig pos, number of positions
disks = [
  (1, 17),
  (0, 7),
  (2, 19),
  (0, 5),
  (0, 3),
  (5, 13)
]

disks_part2 = disks + [(0, 11)]

test_disks = [
  (4,5),
  (1,2)
]


def passes_through(t, disks):
  for d in range(1, len(disks)+1):
    s, P = disks[d-1]
    if ((t + s + d) % P) != 0:
      return False
  return True

import sys
if 'test' in sys.argv:
  disks = test_disks
elif 'p2' in sys.argv:
  disks = disks_part2


t = 0

while True:
  print(t)
  if passes_through(t, disks):
    print(t)
    break
  t += 1