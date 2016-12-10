#!/usr/bin/env python3

import re



class Bot:
  
  def __init__(self, name, rules, bots, value=None):
    self.name = name
    self.value = value
    self.rules = rules
    self.bots = bots
  
  def add_value(self, value):
    if self.value is not None:
      # give to to other bots
      high = value
      low = self.value
      if int(high) < int(low):
        low = value
        high = self.value
        
      if high == '61' and low == '17':
        print('Bot %s handles 17 and 61' % self.name)
      high_bot = self.rules['high']
      low_bot = self.rules['low']
      self.value = None
      self.give_value_to(high_bot, high)
      self.give_value_to(low_bot, low)
    else:
      self.value = value
  
  def give_value_to(self, out, value):
    if out['out'] == 'output':
      print('Bot %s: %s -> output[%s]' %(str(self), str(value), out['to']))
    else:
      self.bots[out['to']].add_value(value)
  
  def __str__(self):
    return self.__repr__()
  
  def __repr__(self):
    return str(self.name)


BOTS = {}
ACTIONS = []

with open('input') as f:
  for line in f:
    line = line.strip()
    if line.startswith('bot'):
      m = re.match('bot (?P<bot>\d+) gives low to (?P<low_out>bot|output) (?P<low>[\d]+) and high to (?P<high_out>bot|output) (?P<high>[\d]+)', line)
      if not m:
        raise Exception('Failed to match: ' + line)
      bot = m.group('bot')
      high = m.group('high')
      low = m.group('low')
      low_out = m.group('low_out')
      high_out = m.group('high_out')
        
      b = Bot(name=bot, rules={'high':{'to': high, 'out': high_out}, 'low': {'to': low, 'out': low_out}}, bots=BOTS)
      BOTS[bot] = b
    elif line.startswith('value'):
      m = re.match('value (?P<value>\d+) goes to bot (?P<bot>\d+)', line)
      value = m.group('value')
      bot = m.group('bot')
      ACTIONS.append((bot, value))
    else:
      raise Exception('line: ' + line)

for bot, value in ACTIONS:
  BOTS[bot].add_value(value)