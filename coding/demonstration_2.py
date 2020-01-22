from invisible_cities.dataflow import dataflow as fl

def lost_numbers():
    numbers = [4, 8, 15, 16, 23, 42]
    for number in numbers:
        yield dict(number = number)


def number_adder(y):
    def adder(x):
        return x + y
    return adder


from math import sqrt


add_42    = fl.map(number_adder(42), args="number"   , out="number+42")
take_sqrt = fl.map(            sqrt, args="number+42", out="final result")


do_everything = fl.pipe(add_42, take_sqrt)


def file_writer(file):
    def write(data):
        file.write(f"{data}\n")
    return write


@fl.RESULT
def counter(future):
    count = 0
    try:
        while True:
            yield
            count += 1
    finally:
        future.set_result(count)


count = fl.spy_count()
# and count.sink would be used as a pipe component


def is_even(x):
    return bool(x % 2 == 0)

keep_even = fl.filter(is_even, args="number")


with open("demonstration_0.txt", "w") as file:
    print_  = fl.sink(            print, args="final result")
    write   = fl.sink(file_writer(file), args="final result")

    result = fl.push(source = lost_numbers(),
                     pipe   = fl.pipe(keep_even,
                                      count.spy,
                                      add_42,
                                      take_sqrt,
                                      fl.fork(print_,
                                              write )),
                     result = dict(n_numbers = count.future))

    print(f"We have looped over {result.n_numbers} numbers")
