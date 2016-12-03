#!/usr/in/env python3

count = 0
with open('input') as f:
  for line in f:
    sides = []
    for s in line.strip().split(' '):
      if s:
        sides.append(int(s))
    sides = sorted(sides)
    if sides[0] + sides[1] > sides[2]:
      count += 1

print(count)
    