import pytest
def custom_sum(a, b):
    return a+b


###### EXERCISE 1 ######
"""
Rename the file such that the tests are run with pytest command.
Write a test that will check that the results of  custom_sum function
does not depend on arguments order (use a=1, and b=2)
Write a test to check that for a=1 and b=2 the result is 3.
Run the tests.
"""

##### EXERCISE 2 ######
"""
Instead of repeating a=1 and b=2 over tests write a fixture. Add the same tests using the fixture.
"""
from pytest import fixture


##### EXERCISE 3 ######
"""
The tests that check commutation can accept any argument. Write the same test but using parametrize to input
varius values for a and b
"""

from pytest import mark



######################
#### HYPOTHESIS ######


from hypothesis import strategies as st
from hypothesis import given, assume

from math import sqrt


##### EXERCISE 4 ######
"""
Instead of parametrize use hypothesis strategy (for integers or floats)
"""

##### EXERCISE 5 ######
"""
Write test and approperiate strategy that the sum of any length list of positive integers
is greater than the maximal element
"""


##### EXERCISE 6 ######
"""
Fix the strategy so that the test passes. hint(tupples)
"""

@mark.xfail
@given(st.integers())
def test_input_correct(t):
    assert len(t) == 2
    assert isinstance(t[0], bool)
    assert isinstance(t[1],str)


##### EXERCISE 7 ######
"""
Demonstrates the ussage of map function. Adapt the strategies such that the
square root of the provided example is integer (hint input has to be integer**2)
"""

@mark.xfail
@given(st.integers())
def test_root_integer(num):
    assert int(sqrt(num)) == sqrt(num)


##### EXERCISE 8 ######
"""
Demonstrates the ussage of filter function. Adapt the strategy such that
the test passes.
"""

@mark.xfail
@given(st.integers())
def test_sum_greater(x):
    assert x**2 >10


##### EXERCISE 9 ######
"""
Make a composite strategy such that it returns a tuple (n, lst),
where n is an integer between [1, 10] and lst is a list of integers of length n.
"""

@mark.xfail
@given(st.integers())
def test_custom_strat(t):
    assert len(t) == 2
    assert 1 <= t[0] <= 10
    assert len(t[1]) == t[0]


##### EXERCISE 10 ######
"""
Adapt the previous strategy such that the lst does not contain number n (hint, use assume or filter)
"""

@mark.xfail
@given(st.integers())
def test_custom_strat_adp(t):
    assert len(t) == 2
    assert 1 <= t[0] <= 10
    assert len(t[1]) == t[0]
    assert (t[0] not in t[1])
