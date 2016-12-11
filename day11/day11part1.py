#!/usr/bin/env python3

from queue import Queue


floors = [
  sorted(['PoG', 'ThG', 'ThM', 'PrG', 'RuG', 'RuM', 'CoG', 'CoM']),
  sorted(['PoM', 'PrM']),
  [],
  [] 
]


floors_p2 = [
  sorted(['PoG', 'ThG', 'ThM', 'PrG', 'RuG', 'RuM', 'CoG', 'CoM', 'ElG', 'ElM', 'DlG', 'DlM']),
  sorted(['PoM', 'PrM']),
  [],
  [] 
]

test_floors = [
  sorted(['HeM', 'LeM']),
  ['HeG'],
  ['LeG'],
  []
]






def is_conf_ok(floor):
  generators = []
  chips = []
  for device in floor:
    if device.endswith('G'):
      generators.append(device[0:2])
    else:
      chips.append(device[0:2])
  if len(generators):
    for chip in chips:
      if chip not in generators:
        return False
  return True
  

def get_all_possible_conf(floor):
  confs = []
  for i in range(0, len(floor)-1):
    confs.append((floor[i],))
    for j in range(i, len(floor)):
      dev1 = floor[i]
      dev2 = floor[j]
      if dev1 != dev2:
        if dev1.endswith('M') and dev2.endswith('M'):
          # 2 microchips, ok
          confs.append((dev1, dev2))
        elif dev1.endswith('G') and dev2.endswith('G'):
          confs.append((dev1, dev2))
        elif dev1[0:2] == dev2[0:2]:
          confs.append((dev1, dev2))
  confs.append((floor[-1],))
  return confs


def floor_minus(floor, devices):
  return sorted([i for i in filter(lambda f: f not in devices, floor)])

def floor_add(floor, devices):
  return sorted(floor + [i for i in devices])
  
  
def calc_floors(floors, fromfn, tofn, devices):
  cf = [f for f in floors]
  cf[fromfn] = floor_minus(floors[fromfn], devices)
  cf[tofn] = floor_add(floors[tofn], devices)
  return cf

def allowed_floors(i):
  if i == 0:
    return (1,)
  elif i == 3:
    return (2,)
  else:
    return (i-1, i+1)

def the_same(devs1, devs2):
  if len(devs1) != len(devs2):
    return False
  elif len(devs1) == 1:
    return devs1 == devs2
  else:
    return devs1 == devs2 or devs1 == (devs2[1], devs2[0])

def state(floors, elat):
  return ('%d:'%elat) + '|'.join([''.join(c) for c in floors])


import sys
if 'test' in sys.argv:
  floors = test_floors
  print(is_conf_ok(['HeG', 'HeM', 'LeG']))
  print(get_all_possible_conf(floors[0]))
  #sys.exit(0)

if 'p2' in sys.argv:
  floors = floors_p2

# BFS

q = Queue()
min_steps = None
B = None
played_moves = {state(floors, 0)}

total_on_last_floor = sum([len(f) for f in floors])

for devices in get_all_possible_conf(floors[0]):
  print(devices)
  cfloors = calc_floors(floors, 0, 1, devices)
  print(cfloors[0], ' is ok: ', is_conf_ok(cfloors[0]))
  print(cfloors[1], ' is ok: ', is_conf_ok(cfloors[1]))
  
  if is_conf_ok(cfloors[0]) and is_conf_ok(cfloors[1]):
    print('Move ', devices, ' to floor 1 ', cfloors[1], ' and 0 is ', cfloors[0])
    q.put((devices, cfloors, 1, 0, 1, ['from 0 to 1 dev: %s' % str(devices)]))
    played_moves.add(state(cfloors, 1))
  print('----')

while not q.empty():
  entry = q.get()
  devs, floors, on_floor_number, from_floor_number, steps, backtrack = entry
  curr_floor = floors[on_floor_number]
  if on_floor_number == 3:
    print ('ON 4:', curr_floor, '; steps: ', steps)
    if len(curr_floor) == total_on_last_floor:
      print('All on floor 4. Total steps: ', steps)
      if min_steps is None:
        min_steps = steps
        B = backtrack
      elif min_steps > steps:
        min_steps = steps
        B = backtrack
  
  if min_steps is not None and (steps+1) > min_steps:
    continue
  for i in allowed_floors(on_floor_number):
    for devices in get_all_possible_conf(curr_floor):
      if i == from_floor_number and the_same(devices, devs):
        continue
        
      cfloors = calc_floors(floors, on_floor_number, i, devices)
      
      curr_floor_conf = cfloors[on_floor_number]
      next_floor_conf = cfloors[i]
      if is_conf_ok(curr_floor_conf) and is_conf_ok(next_floor_conf):
        s = state(cfloors, i)
        if s in played_moves:
          continue
        played_moves.add(s)
        #print('To floor ', i, ' -> ', next_floor_conf, ' from loor ',on_floor_number,' -> ', curr_floor_conf )
        q.put((devices, cfloors, i, on_floor_number, steps + 1, backtrack + ['from %d to %d dev: %s' % (on_floor_number, i, devices)]))
  

print('Min steps: ', min_steps)
#print(B)
print('Backtrack:\n', '\n'.join(B))
