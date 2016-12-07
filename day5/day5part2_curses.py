#!/usr/bin/env python3

from curses import wrapper, color_pair, init_pair, init_color, COLOR_YELLOW, COLOR_BLACK, COLOR_GREEN, COLOR_RED, COLOR_WHITE, curs_set
from hashlib import md5
from random import randint

import sys
from threading import Thread, Lock
import time
import signal
from random import randint
import os

os.environ['TERM'] = 'xterm-256color'

INPUT = 'uqwqemis'

SIG = {'stop': False, 'message': 'H A C K I N G'}


def stop_handler(signal, frame):
  SIG['stop'] = True

signal.signal(signal.SIGINT, stop_handler)

def hack_password(seed, cn, writer):
  seq = 0
  count = 0
  password = ['*' for i in range(0, cn)]
  while True:
    hsh = md5( (seed + str(seq)).encode('utf-8') ).hexdigest()
    if hsh[0:5] == '00000':
      pos = int(hsh[5], 16)
      if pos >= 0 and pos < cn and password[pos] == '*':
        c = hsh[6]
        password[pos] = c
        count += 1
    seq += 1
    if seq % 1000 == 0:
      if SIG['stop']:
        break
      cinematic_preview(password, writer)
    if not ('*' in password):
      break
  cinematic_preview(password, writer)
  
    
def cinematic_preview(password, writer):
  s = []
  for c in password:
    if c == '*':
      s.append(('%x'%randint(0,15), 1))
    else:
      s.append((c, 2))
  x = writer.tx//2 - ((len(password)*4)//2)
  y = writer.ty//2 - 1
  writer.print(s, x, y)



class SDisplay:
  """
   _      _  _       _   _   _   _   _   _              _  _
  | |  |  _| _| |_| |_  |_  | | |_| |_| |_| |_   _  _| |_ |_
  |_|  | |_  _|   |  _| |_|   | |_|  _| | | |_| |_ |_| |_ |
  
  """
  HEX = {
    '0': [' _ ', '| |', '|_|'],
    '1': ['   ', '  |', '  |'],
    '2': [' _ ', ' _|', '|_ '],
    '3': [' _ ', ' _|', ' _|'],
    '4': ['   ', '|_|', '  |'],
    '5': [' _ ', '|_ ', ' _|'],
    '6': [' _ ', '|_ ', '|_|'],
    '7': [' _ ', '| |', '  |'],
    '8': [' _ ', '|_|', '|_|'],
    '9': [' _ ', '|_|', ' _|'],
    'a': [' _ ', '|_|', '| |'],
    'b': ['   ', '|_ ', '|_|'],
    'c': ['   ', ' _ ', '|_ '],
    'd': ['   ', ' _|', '|_|'],
    'e': [' _ ', '|_ ', '|_ '],
    'f': [' _ ', '|_ ', '|  ']
  }
  def __init__(self, stdscr, chars=HEX):
    self.scr = stdscr
    self.chars = chars
    self.lock = Lock()
    ty,tx = stdscr.getmaxyx()
    self.tx = tx
    self.ty = ty
  
  def printc(self, c, x, y):
    char = c
    color = None
    if isinstance(c, tuple):
      char = c[0]
      color = c[1]
    elif isinstance(c, dict):
      char = c['txt']
      color = c['color']
      
    cmap = self.chars[char]
    h = len(cmap)
    w = len(cmap[0])
    for i in range(0, h):
      for j in range(0, w):
        if color is not None:
          self.scr.addstr(y + i, x + j, cmap[i][j], color_pair(color), )
        else:
          self.scr.addstr(y + i, x + j, cmap[i][j])
    return (w, h)
  
  def print(self, msg, x, y):
    self.lock.acquire()
    try:
      for c in msg:
        if isinstance(c, str) and len(c) > 1:
          x, y = self.print(c, x, y)
        else:
          w, h = self.printc(c, x, y)
          x += w
          x += 1
      self.scr.refresh()
      return (x, y)
    finally:
      self.lock.release()
    
    
def print_random_chars(scr, lock, n, tx, ty, sx, sy, sw, sh):
  lock.acquire()
  try:
    
    for i in range(0, n):
      x = randint(1, tx-2)
      y = randint(1, ty-2)
      if (x > sx and x < (sx + sw) )\
         and (y > sy and y < (sy + sh)):
        continue
      color = randint(100, 199)
      c = '%x' % randint(0, 15)
      if randint(0,100) % 2 == 0:
        c = ' '
      scr.addstr(y, x, c, color_pair(color))
    scr.refresh()
  finally:
    lock.release()



def launch_pass_hack(scr):
  try:
    init_pair(1, COLOR_YELLOW, COLOR_BLACK)
    init_pair(2, COLOR_RED, COLOR_BLACK)
    init_pair(3, COLOR_WHITE, COLOR_BLACK)
    init_pair(4, COLOR_GREEN, COLOR_BLACK)
    
    for i in range(0, 100):
      init_color(100+i, i*2, i*2, (i+1)*5 - 1)
      init_pair(100+i, 100+i, COLOR_BLACK)
    
    curs_set(False)
    scr.clear()
    scr.bkgd(' ', color_pair(3)) # init in default
    
    disp = SDisplay(scr)
    ty,tx = scr.getmaxyx()
    hck = 'Hit Ctrl-C to stop the hacking'
    scr.addstr(ty-1, tx-len(hck)-1, hck, color_pair(1))
    
    
    
    message = 'H A C K I N G'
    
    def commence_hack():
      
      if 'test' in sys.argv:
        hack_password('abc', 8, disp)
      else:
        hack_password(INPUT, 8, disp)
      SIG['message'] = '! H A C K E D !'
    
    t = Thread(target=commence_hack)
    t.start()
    
    
    def print_hacked(y):
      c1 = 3
      c2 = 4
      x = tx//2 - len(SIG['message'])//2 - 5
      while True:
        disp.lock.acquire()
        try:
          scr.addstr(y, 0, ''.join([' ' for i in range(0, tx)]), color_pair(c1))
          scr.addstr(y, x, '*** ', color_pair(c1))
          scr.addstr(y, x + 4, SIG['message'], color_pair(c2))
          scr.addstr(y, x + len(SIG['message']) + 4, ' ***', color_pair(c1))
          scr.refresh()
        finally:
          disp.lock.release()
        if SIG['stop']:
          pass
          break
        time.sleep(0.5)
        t = c1
        c1 = c2
        c2 = t
    
    t2 = Thread(target=lambda: print_hacked(ty//2-3))
    t2.start()
    
    def print_rnd():
      while True:
        print_random_chars(scr, disp.lock, 200, tx, ty, tx//2-25, ty//2-6, 50, 12)
        time.sleep(0.1)
        if SIG['stop']:
          break
    
    t3 = Thread(target=print_rnd)
    t3.start()
    
    signal.pause()
    SIG['stop'] = True
    t.join()
    t2.join()
    time.sleep(1)
  finally:
    scr.clear()



wrapper(launch_pass_hack)    
    
    
    
