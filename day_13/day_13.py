from functools import reduce

with open("input") as f:
    earliest_time = int(f.readline())
    bus_times = f.readline().replace("\n", "").split(",")


available_buses = [int(b) for b in bus_times if b != "x"]
cur_min = None
cur_min_index = None
for i, bus_id in enumerate(available_buses):
    waiting_time = ((earliest_time // bus_id) * bus_id + bus_id) - earliest_time
    if cur_min is None or waiting_time < cur_min:
        cur_min = waiting_time
        cur_min_index = i


print("Task 1:", cur_min * available_buses[cur_min_index])


def find_common_period_and_phase(period_i, phase_i, period_j, phase_j):
    gcd, s, t = extended_gcd(period_i, period_j)
    multiplication_factor = (phase_i - phase_j) // gcd

    common_period = period_i // gcd * period_j
    common_phase = (phase_i - s * multiplication_factor * period_i) % common_period
    return common_phase, common_period


def extended_gcd(a, b):
    """shamelessly lifted from wikipedia"""
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        quotient, remainder = divmod(old_r, r)
        old_r, r = r, remainder
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


index_busids_generator = ((i, int(b)) for i, b in enumerate(bus_times) if b != "x")
final_phase, final_period = reduce(
    lambda x, n: find_common_period_and_phase(x[1], x[0], n[1], n[0] % n[1]),
    index_busids_generator,
)
print("Task 2:", -final_phase % final_period)
