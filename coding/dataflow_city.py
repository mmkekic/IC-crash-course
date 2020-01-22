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


def generate_poisson():
    for _ in range(10000):
        yield dict(poisson=np.random.poisson(50))

def polynom(x):
    return x**3 + x**2 +  x

def divisible_by_7(x):
    return x % 7 == 0

def divisible_by_3(x):
    return x % 3 == 0

def not_divisible(x, y):
    return not divisible_by_7(x) and not divisible_by_3(y)

@np.vectorize
def digit_adder(x):
    return sum(map(int, str(x)))

def file_writer(file):
    def write(data):
        file.write(f"{data}\n")
    return write


count_in = fl.spy_count()
count_sl = fl.spy_count()
count_7  = fl.spy_count()
count_3  = fl.spy_count()
count_u  = fl.spy_count()

compute_polynom = fl.map(    polynom, args="poisson", out= "polynom")
sum_digits      = fl.map(digit_adder, args="polynom", out="digitsum")

take_divisible_by_7 = fl.filter(divisible_by_7, args= "polynom")
take_divisible_by_3 = fl.filter(divisible_by_3, args="digitsum")
take_not_divisible  = fl.filter(not_divisible , args=("polynom", "digitsum"))

with open("divisible_by_7.txt", "w") as file7,\
     open("divisible_by_3.txt", "w") as file3,\
     open(       "useless.txt", "w") as fileu:
    write_7  = fl.sink(file_writer(file7), args="poisson")
    write_3  = fl.sink(file_writer(file3), args="polynom")
    write_u  = fl.sink(file_writer(fileu), args="poisson")

    result = fl.push(source = generate_poisson(),
                     pipe   = fl.pipe(count_in.spy,
                                      fl.slice(5, None, 3),
                                      count_sl.spy,
                                      compute_polynom,
                                      sum_digits,
                                      fl.fork((take_divisible_by_7, count_7.spy, write_7),
                                              (take_divisible_by_3, count_3.spy, write_3),
                                              (take_not_divisible , count_u.spy, write_u))),
                     result = dict(n_in = count_in.future,
                                   n_sl = count_sl.future,
                                   n_7  = count_7 .future,
                                   n_3  = count_3 .future,
                                   n_u  = count_u .future))

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
