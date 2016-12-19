#!/usr/bin/env python3

"""
This is the Josephus Problem:
  * Wikipedia: https://en.wikipedia.org/wiki/Josephus_problem
  * Numberphile: https://www.youtube.com/watch?v=uCsD3ZGzMgE
  
The function to calculate the safest place from N soldiers is:
  J(N) = (N - 2^floor(log2(N)))*2 + 1 
"""

from math import floor, log

def josephus_number(n):
  return (n - 2**floor(log(n, 2)))*2 + 1
  
number_of_elves = 3001330

print(josephus_number(number_of_elves))