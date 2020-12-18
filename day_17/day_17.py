from copy import deepcopy
from typing import List, Tuple, Iterable, Any, Optional
import itertools


class GameDimension:
    def __init__(self, iterable: Iterable, default_value: Any = None):
        self._list: list = list(iterable)
        if len(self._list) % 2 == 0 and not len(self._list) == 0:
            raise ValueError("Number of elements must be odd")
        if len(self._list) == 0:
            self._list = [default_value]
        self.midpoint: int = len(self._list) // 2 + 1
        self.default_value: Any = deepcopy(default_value)

    def __iter__(self):
        return self._list.__iter__()

    def __next__(self):
        return self._list.__next__()

    def __len__(self):
        return self._list.__len__()

    def _grow_list(self, n):
        for _ in range(n):
                self._list.insert(0, deepcopy(self.default_value))
                self._list.append(deepcopy(self.default_value))
                self.midpoint += 1

    def __getitem__(self, key):
        if isinstance(key, slice):
            if abs(max(key.start, key.stop)) + self.midpoint > len(self._list):
                self._grow_list(abs(max(key.start, key.stop)) + self.midpoint - len(self._list))
            return self._list[
                key.start + self.midpoint
                if key.start is not None
                else key.start : key.stop + self.midpoint
                if key.stop is not None
                else key.stop : key.step
            ]
        if abs(key) + self.midpoint > len(self._list):
            self._grow_list(abs(key) + self.midpoint - len(self._list))
        return self._list[key + self.midpoint - 1]

    def __setitem__(self, key, value):
        if abs(key) + self.midpoint > len(self._list):
            self._grow_list(abs(key) + self.midpoint - len(self._list))
          
        self._list[key + self.midpoint - 1] = value

    def __repr__(self):
        return f"GD({self._list.__repr__()})"


class Box:
    def __init__(self, position: Tuple[int, int, int], active: bool = False):
        self.active: bool = active
        self.position: Tuple[int, int, int] = position
        self.neighbours: List[Tuple[int, int, int]] = self._get_neighbours(position)

    def _get_neighbours(self, position: Tuple[int, int, int]):
        i, j, k, l = position
        return [
            (i + x, j + y, k + z, l + w)
            for x, y, z, w in itertools.product(range(-1, 2), repeat=4)
            if (x != 0 or y != 0 or z != 0 or w != 0)
        ]

    def __repr__(self):
        return "#" if self.active else "."


class Game:
    def __init__(self, initial_state: List[List[List[Box]]], initial_active: int, occupied_tolerance: int = 4):
        self._game_state: List[List[List[Box]]] = initial_state
        self.occupied_tolerance = occupied_tolerance
        self.swapped: bool = False
        self.n_active: int = initial_active


    def get_active_neighbours(self, box: Box) -> int:
        active = 0
        for x, y, z, w in box.neighbours:
            # print(x,y,z)
            if self._game_state[w][z][y][x] is not None and self._game_state[w][z][y][x].active:
                active += 1
        return active


    def simulate_one_step(self):
        all_n = set()
        for z_axis in self._game_state:
            for y_axis in z_axis:
                for x_axis in y_axis:
                    for box in x_axis:
                        for neighbour in box.neighbours:
                            all_n.add(neighbour)
        # print((-1,3,-1) in all_n)
        # a = deepcopy(self._game_state)
        # print("test,", a[-1])
        #         # print(self._game_state[-1][3][-1])
        for x, y, z, w in all_n:
            if self._game_state[w][z][y][x] is None:
                # print(x,y,z)
                self._game_state[w][z][y][x] = Box((x,y,z,w))
                # print(self._game_state)
            
        # print("eheheh")
        # self.print()
        # print("jehee")
        new_game_state = deepcopy(self._game_state)
        for z_axis in new_game_state:
            for y_axis in z_axis:
                for x_axis in y_axis:
                    for box in x_axis:
                        x, y, z, w = box.position
                        # print(self._get_game_state())
                        
                        active_neighbours = self.get_active_neighbours(box)
                        # assert False
                        if box.active and active_neighbours not in (2, 3):
                            new_game_state[w][z][y][x].active = False
                            self.n_active -= 1
                        if not box.active and active_neighbours == 3:
                            new_game_state[w][z][y][x].active = True
                            self.n_active += 1
        self._game_state = new_game_state

    def simulate(self, steps, _print: bool = True) -> int:
        if _print:
            self.print()
        for i in range(steps):
            print(i)
            self.simulate_one_step()
            if _print:
                self.print()
        return self.n_active

    def get_occupied(self) -> int:
        return self.occupied

    def print(self) -> None:
        print()
        for i, y_axis in enumerate(self._game_state):
            print(i- len(y_axis)//2 + 1)
            for line in y_axis:
                print("".join([Box.__repr__() for Box in line]))
            print()
import os
with open(os.path.abspath("day_17/input")) as f:
    textinput = [list(c.replace("\n", "")) for c in f.readlines()]

initial_game_state = GameDimension([], None)

for i, line in enumerate(textinput):
    if len(textinput[i]) % 2 == 0:
        textinput[i].append(".")
if len(textinput) % 2 == 0:
    textinput.append(["."] * len(textinput[0]))

initial_active = 0
initial_y = GameDimension([], GameDimension([], None))
for j, line in enumerate(textinput):
    normalised_j = j - (len(textinput))//2
    initial_x = GameDimension([], None)
    for i, char in enumerate(line):
        normalised_i = i - (len(line))//2
        if char == "#":
            initial_active += 1
        initial_x[normalised_i] = Box((normalised_i, normalised_j, 0, 0), active=True if char == "#" else False)
    initial_y[normalised_j] = initial_x
initial_z = GameDimension([initial_y], GameDimension([], GameDimension([], None)))
initial_game_state = GameDimension([initial_z], GameDimension([], GameDimension([], GameDimension([], None))))

print(initial_game_state)
# assert False
game = Game(initial_game_state, initial_active)
# game.print()
# game.simulate_one_step()
# game.print()
# game.simulate_one_step()
# game.print()
res = game.simulate(steps=6, _print=False)
print("task 1:", res)
