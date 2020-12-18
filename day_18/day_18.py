import pyparsing
from itertools import chain
import operator
from functools import reduce
from typing import Union

operator_lut = {
    "+": operator.add,
    "*": operator.mul,
}

def evaluate(a: list):
    symbols = a[1::2]
    values = a[::2]
    iterator = zip(symbols, values[1:])
    return reduce(r, iterator, values[0])

def r(a, b):
    _a = a
    if isinstance(a, list):
        _a = evaluate(a)
    operator, value = b
    if isinstance(value, list):
        value = evaluate(value)
    return operator_lut[operator](int(_a), int(value))


def r2(a, b):
    if isinstance(b, list):
        return a + str(evaluate2(b))
    return a + b

def evaluate2(input):
    input_str = reduce(r2, input, "")
    return reduce(operator.mul, (sum(int(i) for i in a.split("+")) for a in input_str.split("*")))


equation = pyparsing.Word(pyparsing.nums) | '+' | '*' 
parens = pyparsing.nestedExpr( '(', ')', content=equation)
grammar = pyparsing.OneOrMore(parens | equation)

with open("input") as f:
    parsed_input = [grammar.parseString(l).asList() for l in f.readlines()]


print("Task 1:", sum((evaluate(line) for line in parsed_input)))

print("Task 2:", sum((evaluate2(line) for line in parsed_input)))