#!/usr/bin/env python3

inp = '^^^^......^...^..^....^^^.^^^.^.^^^^^^..^...^^...^^^.^^....^..^^^.^.^^...^.^...^^.^^^.^^^^.^^.^..^.^'

def next_row(row):
  nr = ''
  for i in range(0, len(row)):
    if i == 0:
      nr = '^' if row[0:2] in ['^^', '.^'] else '.'
    elif i == len(row) - 1:
      nr += '^' if row[-2:] in ['^^', '^.'] else '.'
    else:
      nr += '^' if row[i-1:i+2] in ['^^.', '.^^', '^..', '..^'] else '.'
  return nr

count = 0
n = 40

import sys

if 'p2' in sys.argv:
  n = 400000

row = inp
while n:
  count += sum([1 if i =='.' else 0 for i in row])
  row = next_row(row)
  n -= 1
  print('>', n)
print(count)