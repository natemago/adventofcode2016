#!/usr/in/env python3

rows = []

count = 0
lc = 0

with open('input') as f:
  for line in f:
    sides = []
    lc += 1
    for s in line.strip().split(' '):
      if s:
        sides.append(int(s))
    rows.append(sides)
    if lc == 3:
      for i in range(0,3):
        triangle = sorted([rows[0][i], rows[1][i], rows[2][i]])
        if triangle[0] + triangle[1] > triangle[2]:
          count += 1
      lc = 0
      rows = []
          

print(count)
    