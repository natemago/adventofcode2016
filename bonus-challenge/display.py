#!/usr/bin/env python3

import re

class Display:
  def __init__(self, width, height):
    self.display = [[0 for j in range(0,width)] for i in range(0,height)]
    self.w = width
    self.h = height
  
  def rect(self, a, b):
    for i in range(0, a):
      for j in range(0, b):
        self.display[j][i] = 1
  
  def rotate_row(self, a, b):
    row = [0 for i in range(0, self.w)]
    for i in range(0, self.w):
      row[(i + b) % self.w] = self.display[a][i]
    self.display[a] = row
  
  def rotate_column(self, a, b):
    col = [0 for i in range(0, self.h)]
    for i in range(0, self.h):
      col[(i + b) % self.h] = self.display[i][a]
    
    for i in range(0, self.h):
      self.display[i][a] = col[i]
  
  def __repr__(self):
    r = ''
    for row in self.display:
      r += ''.join(['#' if i else '.' for i in row]) + '\n'
    return r
  
  def __str__(self):
    return self.__repr__()

display = Display(50, 6)


import sys

if 'test' in sys.argv:
  display = Display(7, 3)
  display.rect(3, 2)
  print(display)
  display.rotate_column(1, 1)
  print(display)
  display.rotate_row(0, 4)
  print(display)
  sys.exit(0)



with open('display-input-instructions') as f:
  for line in f:
    line = line.strip()
    if line.startswith('rect'):
      m = re.search('(?P<a>\d+)x(?P<b>\d+)', line)
      a = int(m.group(1))
      b = int(m.group(2))
      display.rect(a, b)
    elif line.startswith('rotate column'):
      m = re.search('x=(?P<a>\d+) by (?P<b>\d+)', line)
      a = int(m.group(1))
      b = int(m.group(2))
      display.rotate_column(a, b)
    elif line.startswith('rotate row'):
      m = re.search('y=(?P<a>\d+) by (?P<b>\d+)', line)
      a = int(m.group(1))
      b = int(m.group(2))
      display.rotate_row(a, b)
    else:
      raise Exception('Invalid line: ' + line)

print('Total on: ', sum([sum(row) for row in display.display]))
print(display)