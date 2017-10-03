#!/usr/bin/env python3

import re
from collections import deque
import sys

class BunnyHQComputer:
  
  def __init__(self, verbose=False):
    self.regs = {'a': 0,'b': 0, 'c': 0, 'd': 0}
    self.mem = []
    self.pc = 0
    self.instr_set = {
      'cpy': self.cpy,
      'inc': self.inc,
      'dec': self.dec,
      'jnz': self.jnz,
      'tgl': self.tgl,
      'out': self.out
    }
    self.instcnt = 0
    self.opthoops = 0
    self.lbb = deque(maxlen=6)
    self.lbbpc = deque(maxlen=6)
    self.transmitted = []
    self.verbose = verbose
  
  def __repr__(self):
    return 'R[%5d|%5d|%5d|%5d] @ %2d - %s' % (self.regs['a'],self.regs['b'],
                                             self.regs['c'],self.regs['d'],
                                             self.pc, self.mem[self.pc] if self.pc >=0 and self.pc < len(self.mem) else 'OUT')
  def stats(self):
    return '%d instuctions executed. Optimized jumps: %d' %(self.instcnt, self.opthoops)
  
  def cpy(self, args):
    x = args[0]
    y = args[1]
    if not y.isalpha():
      self.pc += 1
      return
    if x.isalpha():
      self.regs[y] = self.regs[x]
    else:
      self.regs[y] = int(x)
    
    self.pc += 1
  
  def inc(self, args):
    if not args[0].isalpha():
      self.pc += 1
      return
    self.regs[args[0]] += 1
    self.pc += 1
    
  def dec(self, args):
    if not args[0].isalpha():
      self.pc += 1
      return
    self.regs[args[0]] -= 1
    self.pc += 1
  
  def jnz(self, args):
    x = args[0]
    y = args[1]
    if y.isalpha():
      y = self.regs[y]
    else:
      y = int(y)
    if x.isalpha():
      if self.regs[x]:
        self.pc += y
        return
    else:
      if int(x):
        self.pc += y
        return
    self.pc += 1
  
  def tgl(self, args):
    
    x = args[0]
    if (x+'').isalpha():
      x = self.regs[x]
    if self.pc + x < 0 or self.pc + x >= len(self.mem):
      self.pc += 1
      return
    inst = self.mem[self.pc + x]
    if len(inst) == 2:
      if inst[0] == 'inc':
        inst[0] = 'dec'
      else:
        inst[0] = 'inc'
    else:
      if inst[0] == 'jnz':
        inst[0] = 'cpy'
      else:
        inst[0] = 'jnz'
    self.pc += 1
  
  
  def out(self, args):
    x = args[0]
    if x.isalpha():
      x = self.regs[x]
    else:
      x = int(x)
    self.transmitted.append(x)
    self.pc += 1
    #print('>>>', chr(x))
    print(chr(x), end="")
  
  def log(self, *args):
    if self.verbose:
      print(*args)
  
  def strmem(self):
    return '\n'.join([str(m) for m in self.mem])
  
  
  def opt_lookahead(self):
    # addition
    """
    inc a
    dec c
    jnz c -2
     => a = a + c
    """
    if self.pc + 2 < len(self.mem):
      instrs = self.mem[self.pc:self.pc+3]
      i_str = ' '.join([' '.join(i) for i in instrs])
      m = re.match(r'inc (\w) dec (\w) jnz \2 -2', i_str)
      if m:
        # addition
        x = m.group(1)
        y = m.group(2)
        
        self.regs[x] += self.regs[y]
        self.regs[y] = 0
        self.pc += 3
        self.log('opt_add', x, '=', x, '+', y, self.regs,'; pc=', self.pc)
        self.lbb.append(['inc', x])
        self.lbb.append(['dec', y])
        self.lbb.append(['jnz', y, '-2'])
        self.lbbpc.append(self.pc-2)
        self.lbbpc.append(self.pc-1)
        self.lbbpc.append(self.pc)
        return True
        
    return False
  
  def opt_lookbehind(self):
    #return False
    self.lbb.append(self.mem[self.pc])
    self.lbbpc.append(self.pc)
    instr = ' '.join([' '.join(i) for i in list(self.lbb)])
    m = re.match(r'cpy ([\w\d]+) (\w) inc (\w) dec (\w) jnz \4 -2 dec (\w) jnz \5 -5', instr)
    if m:
      v = m.group(1) # 182
      d = m.group(2) # b
      x = m.group(3) # d
      y = m.group(4) # b
      c = m.group(5) # c
      # 'c': 13, 'd': 184, 'a': 2, 'b': 0
      
      if v.isalpha():
        v = self.regs[v]
      else:
        v = int(v)
      
      xv = self.regs[x]
      result = self.regs[c]*v + xv
      self.regs[c] = 0
      self.regs[y] = 0
      self.regs[x] = result
      
      # c <- 0, {'c': 0, 'd': 2550, 'a': 2, 'b': 0} to pc 9
      self.pc = self.lbbpc[0] + 6
      
      self.log('opt_mul', x,'=', v,'*',c,'+',x, '->', self.regs, 'PC:', self.pc)
    
    return False
    
  def exec(self):
    inc = 0
    while True:
      inc += 1
      if inc % 10000 == 0:
        #print(computer)
        pass
      if self.pc < 0 or self.pc >= len(self.mem):
        break
      if self.opt_lookahead() or self.opt_lookbehind():
        self.opthoops += 1
        continue
      instr = self.mem[self.pc]
      op = self.instr_set[instr[0]]
      try:
        op(instr[1:])
        self.log(' '.join(instr), '  >>', self.regs , 'PC:', self.pc, '; out:', self.transmitted)
      except:
        print ('Failure on instruction:',instr)
        raise
      self.instcnt += 1
    


def read_program(inpf):
  mem= []
  with open(inpf) as f:
    for line in f:
      instr = line.strip().split(' ')
      #print(instr)
      mem.append(instr)
  return mem

verbose = False

if 'verbose' in sys.argv:
  verbose = True

computer = BunnyHQComputer(verbose=verbose)


mem = read_program('bonus-challenge-input')
computer.mem = mem

"""

"""

computer.regs['a'] = 0

if 'solve' in sys.argv:
  computer.regs['a'] = 182


computer.exec()

"""
If you print out the instructions for a = 0, you'll get this repeting pattern:
  cpy 2 c   >> {'a': 0, 'd': 2548, 'c': 2, 'b': 2548} PC: 13 ; out: []
  jnz b 2   >> {'a': 0, 'd': 2548, 'c': 2, 'b': 2548} PC: 15 ; out: []
  dec b   >> {'a': 0, 'd': 2548, 'c': 2, 'b': 2547} PC: 16 ; out: []
  dec c   >> {'a': 0, 'd': 2548, 'c': 1, 'b': 2547} PC: 17 ; out: []
  jnz c -4   >> {'a': 0, 'd': 2548, 'c': 1, 'b': 2547} PC: 13 ; out: []
  jnz b 2   >> {'a': 0, 'd': 2548, 'c': 1, 'b': 2547} PC: 15 ; out: []
  dec b   >> {'a': 0, 'd': 2548, 'c': 1, 'b': 2546} PC: 16 ; out: []
  dec c   >> {'a': 0, 'd': 2548, 'c': 0, 'b': 2546} PC: 17 ; out: []
  jnz c -4   >> {'a': 0, 'd': 2548, 'c': 0, 'b': 2546} PC: 18 ; out: []
  inc a   >> {'a': 1, 'd': 2548, 'c': 0, 'b': 2546} PC: 19 ; out: []
  jnz 1 -7   >> {'a': 1, 'd': 2548, 'c': 0, 'b': 2546} PC: 12 ; out: []


which basically divides d with 2 (integer division).
Now just before outputing a value, we can see:

jnz 1 -7   >> {'a': 1274, 'd': 2548, 'c': 0, 'b': 0} PC: 12 ; out: [] - this is the end of the pattern, with the division result in a

and:

further bellow:


cpy 2 c   >> {'a': 1274, 'd': 2548, 'c': 2, 'b': 0} PC: 13 ; out: []
jnz b 2   >> {'a': 1274, 'd': 2548, 'c': 2, 'b': 0} PC: 14 ; out: []
jnz 1 6   >> {'a': 1274, 'd': 2548, 'c': 2, 'b': 0} PC: 20 ; out: []
cpy 2 b   >> {'a': 1274, 'd': 2548, 'c': 2, 'b': 2} PC: 21 ; out: []
jnz c 2   >> {'a': 1274, 'd': 2548, 'c': 2, 'b': 2} PC: 23 ; out: []
dec b   >> {'a': 1274, 'd': 2548, 'c': 2, 'b': 1} PC: 24 ; out: []
dec c   >> {'a': 1274, 'd': 2548, 'c': 1, 'b': 1} PC: 25 ; out: []
jnz 1 -4   >> {'a': 1274, 'd': 2548, 'c': 1, 'b': 1} PC: 21 ; out: []
jnz c 2   >> {'a': 1274, 'd': 2548, 'c': 1, 'b': 1} PC: 23 ; out: []
dec b   >> {'a': 1274, 'd': 2548, 'c': 1, 'b': 0} PC: 24 ; out: []
dec c   >> {'a': 1274, 'd': 2548, 'c': 0, 'b': 0} PC: 25 ; out: []
jnz 1 -4   >> {'a': 1274, 'd': 2548, 'c': 0, 'b': 0} PC: 21 ; out: []
jnz c 2   >> {'a': 1274, 'd': 2548, 'c': 0, 'b': 0} PC: 22 ; out: []
jnz 1 4   >> {'a': 1274, 'd': 2548, 'c': 0, 'b': 0} PC: 26 ; out: []
jnz 0 0   >> {'a': 1274, 'd': 2548, 'c': 0, 'b': 0} PC: 27 ; out: [] - which basically does nothing, but outputs whatever is leftover from b


out b   >> {'a': 1274, 'd': 2548, 'c': 0, 'b': 0} PC: 28 ; out: [0]

Then we jump way back, copy the value from a to b, and repeat pattern 1:
cpy 2 c   >> {'a': 0, 'd': 2548, 'c': 2, 'b': 1274} PC: 13 ; out: [0]
...
After the division, we end up with 0 in b and the out is [0,0]
a=1274/2=637, b is zero (no leftover fromthe division)
the next division will yield 1, sothe output will be 1 and a should be = 318 (637/2)
out b   >> {'a': 318, 'd': 2548, 'c': 0, 'b': 1} PC: 28 ; out: [0, 0, 1]


Bascaly this procedure converts the number N+2548 into binary.

In order to generate a signal like 0,1,0,1,0.... we need to find the smallest N
that N+2548 in binary looks like thesignal.
2548 in binary is: 0000100111110100
The nearest number matching the signal is:
0000100111110100 (2548)
0000101010101010 (2730)

2730-2548 = 182
"""


  