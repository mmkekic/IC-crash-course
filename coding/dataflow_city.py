"""
Build a city that has:
- Source: 1e4 random numbers following a Poisson(50)
- Pipes:
    - Count events in
    - Slice to keep only every 3rd number starting from the 5th one
    - Count events after slicing
    - Compute x + x**2 + x**3
    - If the result is divisible by 7 save the original number to divisible_by_7.txt
    - If the sum of the digits is divisible by 3 save the modified number to divisible_by_3.txt
    - If neither condition is satisfied save the original number to useless.txt
    - Add counters to check how many numbers satisfy each condition

EXTRA:
    - Write a test :)
"""

import numpy as np

from invisible_cities.dataflow import dataflow as fl

np.random.seed(314159265)

##############################################################################
# Write here your city
# push output should be assigned to a variable named result.
# result should contain, at least 5 things: n_in, n_sl, n_7, n_3 and n_u,
# which are the counters described in the exercise.
# When you are finished run `python dataflow_city.py` and check that
# the code runs and the tests pass!
##############################################################################





##############################################################################
# Tests
##############################################################################

def read(filename):
    return np.loadtxt(filename, dtype=int)

# tests
def tests():
    assert result.n_in == int(1e4)
    assert result.n_sl == (int(1e4) - 5) // 3 + 1
    assert result.n_7  == 1429
    assert result.n_3  == 2200
    assert result.n_u  ==  662
    assert all(polynom    (read("divisible_by_7.txt")) % 7 == 0)
    assert all(digit_adder(read("divisible_by_3.txt")) % 3 == 0)
    assert all(polynom    (read(       "useless.txt")) % 7 != 0)
    assert all(digit_adder(read(       "useless.txt")) % 3 != 0)
    print("All tests passed!")

tests()
