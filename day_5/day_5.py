seats = [
    int(line[:-4].replace("B", "1").replace("F", "0"), 2) * 8 + int(line[-4:].replace("R", "1").replace("L", "0"), 2)
    for line in open("input").readlines()
]
print("Task 1", max(seats))
n = len(seats)
min_ = min(seats)
total = (n + min_) * (n + min_ + 1) / 2
print("Task 2", total - sum(seats) - (min_ - 1) * min_ / 2)
