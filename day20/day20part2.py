#!/usr/bin/env python3

intervals = []

with open('input') as f:
  for line in f:
    line = line.strip().split('-')
    start = int(line[0])
    end = int(line[1])
    intervals.append((start, end))


intervals = sorted(intervals, key=lambda x: x[0])

prev = (0,0)
alowed = 0
for i in range(0, len(intervals)):
  px, py = prev
  cx, cy = intervals[i]
  if not (cx-1) <= py:
      print(px,py, '|', cx, cy, ' = ', cx-py-1)
      alowed += (cx-py-1)
      prev = intervals[i]
  else:
    prev = (px, max(cy, py))
alowed += 4294967295 - prev[1]
print('Alowed IPs count: ', alowed)