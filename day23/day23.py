#!/usr/bin/env python3

from collections import deque

class BunnyHQComputer:
  
  def __init__(self):
    self.regs = {'a': 0,'b': 0, 'c': 0, 'd': 0}
    self.mem = []
    self.pc = 0
    self.instr_set = {
      'cpy': self.cpy,
      'inc': self.inc,
      'dec': self.dec,
      'jnz': self.jnz,
      'tgl': self.tgl
    }
    self.instcnt = 0
    self.opthoops = 0
    self.lbb = deque(maxlen=5)
    self.lbbpc = deque(maxlen=5)
  
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
      if instrs == [['inc','a'],['dec','c'],['jnz','c','-2']]:
        self.regs['a'] += self.regs['c']
        self.regs['c'] = 0
        self.pc += 3
        return True
      elif instrs == [['inc','a'],['dec','d'],['jnz','d','-2']]:
        self.regs['a'] += self.regs['d']
        self.regs['d'] = 0
        self.pc += 3
        return True
        
    return False
  
  def opt_lookbehind(self):
    #return False
    self.lbb.append(self.mem[self.pc])
    self.lbbpc.append(self.pc)
    #print(self.lbb)
    if list(self.lbb)[-3:] == [['dec', 'd'],['jnz', 'd', '-5'],['cpy', 'b','c']]:
        """
        a = b * d
        c = 0
        d = 0 
        PC = PC + 1
        """
        self.regs['a'] = self.regs['b'] * (self.regs['d']+1)
        self.regs['c'] = 0
        self.regs['d'] = 0
        self.pc = self.lbbpc[-3] + 2
        
        #self.lbb = deque(maxlen=5)
        #self.lbbpc = deque(maxlen=5)
        
        #print(self, self.lbbpc, self.lbb)
        #raise Exception('OPTLB')
        return True
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
        print('OPT JUMP -> ', self)
        self.opthoops += 1
        continue
      instr = self.mem[self.pc]
      op = self.instr_set[instr[0]]
      try:
        op(instr[1:])
        print(' '.join(instr), '  >>', self.regs , 'PC:', self.pc)
      except:
        print ('Failure on instruction:',instr)
        raise
      self.instcnt += 1
    


def read_program(inpf):
  mem= []
  with open(inpf) as f:
    for line in f:
      instr = line.strip().split(' ')
      print(instr)
      mem.append(instr)
  return mem


computer = BunnyHQComputer()
import sys
if 'test' in sys.argv:
  mem = read_program('test_input')
else:
  mem = read_program('input')
computer.mem = mem

"""
for i in [7,5,3]:
  computer = BunnyHQComputer()
  computer.mem = mem
  computer.regs['a'] = i
  print(i)
  computer.exec()
  print(i, ' -> ', computer)  



sys.exit(0)
"""
computer.regs['a'] = 7

if 'p2' in sys.argv:
  computer.regs['a'] = 12

computer.exec()

print('------------------------')
print('Final state:', computer)
print('Stats: ', computer.stats())
print('Key:', computer.regs['a'])


  