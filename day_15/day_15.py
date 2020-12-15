from itertools import count, islice

def number_generator(input: list):
    if len(input) < 2:
        raise ValueError
    spoken_numbers = {n: i+1 for i, n in enumerate(input[:-1])}
    last_number = input[-1]
    for i in input:
        yield i
    for i in count(len(input)):
        if last_number in spoken_numbers.keys():
            cur_value = i - spoken_numbers[last_number]
        else:
            cur_value = 0
        spoken_numbers[last_number] = i
        last_number = cur_value
        yield cur_value

input = [0,13,1,16,6,17]
print("Task 1:", next(islice(number_generator(input), 2020-1, None)))
print("Task 2:", next(islice(number_generator(input), 30000000-1, None)))