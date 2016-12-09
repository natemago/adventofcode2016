#!/usr/bin/env python3

import re
import sys


inp_file = 'input'

if 'test' in sys.argv:
  inp_file = 'test-input'


decompressed = ''

def count_decompressed(fac, token):
  tot = 0
  marker = ''
  i = 0
  while i < len(token):
    c = token[i]
    if c == '(' and not marker:
      marker = '('
    elif c == ')' and marker:
      """
      Doing a leap of faith here:
        - assuming that the part of the string that should be repeated after this
        marker will always be of the form: (marker)(marker2)...(markerN)SOME_STRING
        i.e all the markers are consecuitive at the begining of the token.
      """
      sub = token[i+1:]
      marker = marker[1:]
      marker = marker.split('x')
      cnt = int(marker[0])
      rep = int(marker[1])
      sub = sub[0:cnt]
      tot += count_decompressed(rep, sub)
      token = token[i+1+cnt:]
      i = 0
      marker = ''
      continue
    elif marker:
      marker += c
    else:
      if c not in ' \n\r\t':
        tot += 1
    i += 1
      
      
  return tot*fac

total = 0
gc = 0
with open(inp_file) as f:
  compressed = f.read()
  total = count_decompressed(1, compressed)

print (total)
