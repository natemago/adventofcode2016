#!/usr/bin/env python3

intervals = []

with open('input') as f:
  for line in f:
    line = line.strip().split('-')
    start = int(line[0])
    end = int(line[1])
    intervals.append((start, end))


intervals = sorted(intervals, key=lambda x: x[0])

prev = intervals[0]

for i in range(1, len(intervals)):
  print(' > p:', prev)
  px, py = prev
  cx, cy = intervals[i]
  print(' > c:', intervals[i])
  if not (cx-1) <= py:
      print(py+1)
      break
  else:
    prev = (px, max(cy, py))
    