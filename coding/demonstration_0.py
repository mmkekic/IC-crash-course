from invisible_cities.dataflow import dataflow as fl


def lost_numbers():
    numbers = [4, 8, 15, 16, 23, 42]
    for number in numbers:
        yield {"number": number}
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

with open("demonstration_0.txt", "w") as file:
    print_  = fl.sink(            print, args="final result")
    write   = fl.sink(file_writer(file), args="final result")

    fl.push(source = lost_numbers(),
            pipe   = fl.pipe(fl.spy(print),
                             add_42,
                             fl.spy(print),
                             take_sqrt,
                             fl.spy(print),
                             fl.fork(print_,
                                     write)),
            result = ())
