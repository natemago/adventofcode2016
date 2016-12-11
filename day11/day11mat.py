#!/usr/bin/env python3
"""
If we analyze the problem in term of number of moves needed to lift n objects
1 floor up, we can see that:

n | # moves
--+-------
2 | 1  (both up)
3 | 3  (*)
4 | 5  (*)

(*) - Note that this required some work on paper to see the number of moves :) 

We can express this like so:

M(n) - number of moves as function of number of objects

M(2) = 1
M(n) = M(n-1) + 2

If we expand with substitution for (n-1), then we get:
M(n) = M(n-1) + 2 = 
     = M(n-2) + 2 + 2 = M(n-2) + 2*2 =
     = M(n-3) + 2 + 2 + 2 = M(n-3) + 2*3
     = M(n-i) + 2*i

Now let's subs. for i = n-2
M(n) = M(n - (n-2) ) + 2*(n-2) = 
M(n) = M(2) + 2*(n-2) // subs 1 for M(2)
M(n) = 1 + 2*(n-2)


This is for one floor up. 
For k floor up, we have: 
  C(n,k) = k*M(n)

When we have different number of items on more than one floor, we can do the following:

1. We calculate the steps with M(n) for number of items on floor k to floor k+1
2. Now the number of items on floor k+1 is bigger
3. Go to floor k+1 and repeat 1 (but now for going from floor k+1 to k+2)
4. If we have reached the top, print the total number


Note that this works when we can actually move the inputs to the upper floor without
violating the rules. There may be actually confiurations where this is not possible - 
like in the test input. But we can rearrange the test input so it starts with
a possible configuration as so:

F4: . . . .
F3: HeM, LeM
F2: HeC, LeC
F1: . . . .

This was done using 5 moves, so we need to add 5 more when calculating.

"""



floors_p1 = [8, 2, 0] # input was valid
floors_p2 = [12, 2, 0] # input was valid

test_floors = [0, 2, 2] # needed some rearrangement with 5 extra steps

def M(n):
  if n == 0:
    return 0
  return 2*(n-2) + 1

def calc_all(floors):
  floor_items_count = 0
  total = 0
  for number_of_objects in floors:
    floor_items_count += number_of_objects
    total += M(floor_items_count)
  return total
  
  
print('Test: ', 5 + calc_all(test_floors))
print('Part 1: ', calc_all(floors_p1))
print('Part 2: ', calc_all(floors_p2))

