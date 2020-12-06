from functools import reduce
with open("input") as f:
    input_ = f.read()[:-1].split("\n\n")
print("task 1:", sum([len(set(resp.replace("\n", "")))for resp in input_]))
print("task 2:", sum([len((reduce(lambda x, y: set(x).intersection(set(y)), group_resp.split("\n")))) for group_resp in input_]))
