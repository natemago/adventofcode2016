#!/usr/bin/env python3

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
  
  def __repr__(self):
    return 'R[%5d|%5d|%5d|%5d] @ %2d - %s' % (self.regs['a'],self.regs['b'],
                                             self.regs['c'],self.regs['d'],
                                             self.pc, self.mem[self.pc] if self.pc >=0 and self.pc < len(self.mem) else 'OUT')
  
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
  
  def exec(self):
    inc = 0
    while True:
      inc += 1
      if inc % 10000 == 0:
        print(computer)
      if self.pc < 0 or self.pc >= len(self.mem):
        break
      instr = self.mem[self.pc]
      op = self.instr_set[instr[0]]
      try:
        #print(self)
        op(instr[1:])
        #print(self)
      except:
        print ('Failure on instruction:',instr)
        raise


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

computer.regs['a'] = 7

if 'p2' in sys.argv:
  computer.regs['a'] = 12

computer.exec()

print('------------------------')
print('Final state:', computer)
print('Key:', computer.regs['a'])

  