#!/usr/bin/env python3

keypad = ['123','456','789']

def move(pos, d):
  r = [pos[0] + d[0], pos[1] + d[1]]
  if r[0] > 1 or r[0] < -1 or r[1] > 1 or r[1] < -1:
    return pos
  return r

def decode_key(pos):
  pos = [pos[0] + 1, pos[1] + 1]
  return keypad[2 - pos[1]][pos[0]]


def print_keypad(pos):
  keypad = [[1,2,3],[4,5,6],[7,8,9]]
  pos = [pos[0] + 1, pos[1] + 1] # translate +1,+1
  pos = [2-pos[1], pos[0]] # flip the y-axis
  keypad[pos[0]][pos[1]] = '\x1b[31m%d\x1b[0m' % keypad[pos[0]][pos[1]]
  print('+-------+')
  for p in keypad:
    print('|',' '.join([str(a) for a in p]),'|')
  print('+-------+')
  print()
  
def decode(pos, line):
  for i in line:
    #print(' [', i, ']')
    if i == 'U':
      pos = move(pos, [0,1])
    elif i =='D':
      pos = move(pos, [0,-1])
    elif i == 'L':
      pos = move(pos, [-1,0])
    elif i == 'R':
      pos = move(pos, [1,0])
    else:
      raise Exception(i)
      
  return pos


import sys

if 'test' in sys.argv:
  test_pos = [0,0]
  test_lines = ['ULL','RRDDD','LURDL','UUUUD']
  for l in test_lines:
    test_pos = decode(test_pos, l)
    print(decode_key(test_pos))
  
  sys.exit(0)




code = ''
pos = [0,0]
with open('input') as f:
  for line in f:
    line = line.strip()
    pos = decode(pos, line)
    code += decode_key(pos)
    print_keypad(pos)

print(code)