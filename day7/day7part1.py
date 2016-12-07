#!/usr/bin/env python3

import re

count = 0

with open('input') as f:
  for line in f:
    line = line.strip()
    m = re.search(r'(.)(.)\2\1', line)
    if m:
      if not re.search(r'\[[^\[\]]{0,}(.)(.)\2\1[^\[\]]{0,}\]', line):
        if m.group(1) != m.group(2):
          count += 1
print(count)
