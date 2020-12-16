from functools import reduce
import operator

with open("input") as f:
    textinput = f.read()

parameters, my_ticket, other_tickets = textinput.split("\n\n")

values_dict = {}

my_ticket_values = [int(i) for i in my_ticket.split(":")[1].split(",")]
other_tickets_values = [[int(i) for i in j.split(",")] for j in other_tickets.split("\n")[1:] if j != ""]

for line in parameters.split("\n"):
    field_name, values = line.split(": ")
    values_list = ((int(i[0]), int(i[1])) for i in (l.split("-") for l in values.split(" or ")))
    for start, end in values_list:
        for i in range(start, end + 1):
            values_dict.setdefault(i, set()).add(field_name)

scanning_error_rate = reduce(
    operator.add, (value for values in other_tickets_values for value in values if value not in values_dict.keys())
)
print("Task 1:", scanning_error_rate)

possible_fields_by_position = {}
for values in other_tickets_values:
    if any(i not in values_dict.keys() for i in values):
        continue
    for i, value in enumerate(values):
        if i not in possible_fields_by_position.keys():
            possible_fields_by_position[i] = values_dict[value]
        else:
            possible_fields_by_position[i] = possible_fields_by_position[i].intersection(values_dict[value])

good_possible_fields = set()
while len(possible_fields_by_position.keys()) != len(good_possible_fields):
    for i, (_, fields) in enumerate(possible_fields_by_position.items()):
        if len(fields) == 1:
            good_possible_fields = good_possible_fields.union(fields)
        else:
            possible_fields_by_position[i] -= good_possible_fields

task2_result = reduce(
    operator.mul,
    (
        my_ticket_values[position]
        for position, value in possible_fields_by_position.items()
        if list(value)[0].startswith("departure")
    ),
    1,
)

print("Task 2:", task2_result)
