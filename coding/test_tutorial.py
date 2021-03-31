from pytest import mark

import numpy as np


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

def test_custom_sum_1_2():
    assert custom_sum(1, 2) == 3

def test_custom_sum_argument_order():
    assert custom_sum(1, 2) == custom_sum(2, 1)

##### EXERCISE 2 ######
"""
Instead of repeating a=1 and b=2 over tests write a fixture. Add the same tests using the fixture.
"""

from pytest import fixture

@fixture
def one_two():
    return 1, 2

def test_custom_sum_1_2_fixture(one_two):
    one, two = one_two
    assert custom_sum(one, two) == 3

##### EXERCISE 3 ######
"""
The tests that check commutation can accept any argument. Write the same test but using parametrize to input
varius values for a and b
"""

from pytest import mark

@mark.parametrize("a", np.random.randint(-100, 100, 20))
@mark.parametrize("b", np.random.randint(-100, 100, 20))
def test_custom_sum_parametrized(a, b):
    assert custom_sum(a, b) == custom_sum(b, a) == a + b

######################
#### HYPOTHESIS ######


from hypothesis import strategies as st
from hypothesis import given, assume

from math import sqrt


##### EXERCISE 4 ######
"""
Instead of parametrize use hypothesis strategy (for integers or floats)
"""

@given(a = st.integers(),
       b = st.integers())
def test_custom_sum_hypothesis(a, b):
    assert custom_sum(a, b) == a + b

##### EXERCISE 5 ######
"""
Write test and approperiate strategy that the sum of any length list of positive integers
is greater than the maximal element
"""

@st.composite
def lists_of_integers(draw):
    loi = draw(st.lists(st.integers(min_value=1), min_size=2))
    return loi, max(loi)

@given(lists_of_integers())
def test_sum_list_greater_than_max_element(loi_and_max):
    loi, max = loi_and_max
    assert sum(loi) > max


##### EXERCISE 6 ######
"""
Fix the strategy so that the test passes. hint(tupples)
"""

@given(st.tuples(st.booleans(), st.text()))
def test_input_correct(t):
    assert len(t) == 2
    assert isinstance(t[0], bool)
    assert isinstance(t[1],str)


##### EXERCISE 7 ######
"""
Demonstrates the ussage of map function. Adapt the strategies such that the
square root of the provided example is integer (hint input has to be integer**2)
"""

@given(st.integers().map(lambda x: x**2))
def test_root_integer(num):
    assert int(sqrt(num)) == sqrt(num)


##### EXERCISE 8 ######
"""
Demonstrates the ussage of filter function. Adapt the strategy such that
the test passes.
"""

@given(st.integers().filter(lambda x: np.abs(x) > 3))
def test_sum_greater(x):
    assert x**2 >10


##### EXERCISE 9 ######
"""
Make a st.composite strategy such that it returns a tuple (n, lst),
where n is an integer between [1, 10] and lst is a list of integers of length n.
"""

@st.composite
def lists_and_lengths(draw):
    length = draw(st.integers(min_value=1, max_value=10))
    list   = draw(st.lists(st.integers(), min_size = length, max_size = length))
    return length, list

@given(lists_and_lengths())
def test_custom_strat(t):
    assert len(t) == 2
    assert 1 <= t[0] <= 10
    assert len(t[1]) == t[0]


##### EXERCISE 10 ######
"""
Adapt the previous strategy such that the lst does not contain number n (hint, use assume or filter)
"""

@st.composite
def lists_and_lengths_without_length(draw):
    length = draw(st.integers(min_value=1, max_value=10))
    list   = draw(st.lists(st.integers(), min_size = length, max_size = length))
    assume(length not in list)
    return length, list


@given(lists_and_lengths_without_length())
def test_custom_strat_adp(t):
    assert len(t) == 2
    assert 1 <= t[0] <= 10
    assert len(t[1]) == t[0]
    assert (t[0] not in t[1])
