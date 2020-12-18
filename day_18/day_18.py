import pyparsing
from itertools import chain
import operator
from functools import reduce
from typing import Union
equation = pyparsing.Word(pyparsing.nums) | '+' | '*' 
parens = pyparsing.nestedExpr( '(', ')', content=equation)
grammar = pyparsing.OneOrMore(parens | equation)

with open("input") as f:
    parsed_input = [grammar.parseString(l).asList() for l in f.readlines()]

operator_lut = {
    "+": operator.add,
    "*": operator.mul,
}

def r(a, b) -> int:
    _a = a
    if isinstance(a, list):
        symbols = a[1::2]
        values = a[::2]
        iterator = zip(symbols, values[1:])
        _a = reduce(r, iterator, values[0])
    operator, value = b
    if isinstance(value, list):
        symbols = value[1::2]
        values = value[::2]
        iterator = zip(symbols, values[1:])
        value = reduce(r, iterator, values[0])
    return operator_lut[operator](int(_a), int(value))

results = []
for input_line in parsed_input:
    symbols = input_line[1::2]
    values = input_line[::2]
    iterator = zip(symbols, values[1:])
    results.append(reduce(r, iterator, values[0]))
print("Task 1:", sum(results))


def r2(a:str, b: Union[str, list]) -> int:
    if isinstance(b, list):
        return a + str(evaluate(b))
    return a + b

def evaluate(input: list) -> int:
    input_str = reduce(r2, input, "")
    return reduce(operator.mul, (sum(int(i) for i in a.split("+")) for a in input_str.split("*")))

print("Task 2:", sum((evaluate(line) for line in parsed_input)))