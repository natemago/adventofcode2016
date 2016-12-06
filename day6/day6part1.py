#!/usr/bin/env python3

stats = {}

with open('input') as f:
  for line in f:
    line = line.strip()
    i = 0
    for c in line:
      c_stat = stats.get(i)
      if not c_stat:
        c_stat = stats[i] = {}
      if not c_stat.get(c):
        c_stat[c] = 0
      c_stat[c] += 1
      i += 1

message = ''
for i in range(0, len(stats)):
  message += max([(c,cnt) for c,cnt in stats[i].items()], key=lambda k: k[1])[0]

print(message)

