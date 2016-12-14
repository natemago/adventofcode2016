#!/usr/bin/env python3


from hashlib import md5
import re
from threading import Thread


inp = 'ahsbgdzn'

class OTPKeyGenerator:
  def __init__(self, salt=inp, num_hashes=1, init_first=0):
    self.index = 0
    self.salt = salt
    self.num_hashes = num_hashes
    self.cache = {}
    if init_first:
      self.init_first(init_first)
  
  
  def init_first(self, n):
    for i in range(0, n):
      self.cache[i] = self.hsh(i)
      print(i)
  
  def hsh(self, idx):
    hsh = self.cache.get(idx)
    if hsh:
      return hsh
    n = self.num_hashes
    hsh = self.salt + str(idx)
    while n:
      hsh = md5((hsh).encode('utf-8') ).hexdigest()
      n -= 1
    self.cache[idx] = hsh
    return hsh
  
  def is_key(self, hsh, idx, rch):
    chrseq = ''.join([rch for i in range(0,5)])
    for i in range(idx+1, idx+1001):
      if chrseq in self.hsh(i):
        return True
    return False
  
  def next_key(self):
    while True:
      hsh = self.hsh(self.index)
      m = re.search(r'(.)\1\1', hsh)
      if m:
        rch = m.group(1)
        if self.is_key(hsh, self.index, rch):
          self.index += 1
          return hsh
      self.index += 1


nh = 1
import sys

if 'part2' in sys.argv:
  nh = 2017 # 2016 + the first hashing
initfirst = 0
if 'initfirst' in sys.argv:
  initfirst = int(sys.argv[-1])

g = OTPKeyGenerator(num_hashes=nh, init_first=initfirst)
cnt = 0

while True:
  key = g.next_key()
  print(key, ' at ', g.index-1)
  cnt += 1
  if cnt == 64:
    break
print(g.index-1)