from collections import Counter, defaultdict, deque


def task_1(input):
    seen = defaultdict(int, Counter(input[:25]))

    for i, n in enumerate(input[25:]):
        for seen_n in seen.keys():
            if n - seen_n in seen.keys():
                break
        else:
            return n
        seen[n] += 1
        number_out_of_scope = input[i]
        if seen[number_out_of_scope] == 1:
            del seen[number_out_of_scope]
        else:
            seen[number_out_of_scope] -= 1


def task_2(input, target):
    queue = deque()
    sum = 0
    i = 0
    for num in input:
        sum += num
        queue.appendleft(num)
        while sum > target:
            sum -= queue.pop()
        if sum == target:
            return max(queue) + min(queue)
        i += 1


with open("input") as f:
    input = [int(line) for line in f.readlines()]

task1_result = task_1(input)
print("Task 1:", task1_result)
print("Task 2:", task_2(input, task1_result))
