from copy import deepcopy
from typing import List, Tuple
import itertools


class Tile:
    def __init__(self, value: str, neighbours: List[Tuple[int, int]]):
        self.value: str = value
        self.neighbours: List[Tuple[int, int]] = neighbours


class Game:
    def __init__(self, initial_state: List[List[Tile]], occupied_tolerance: int = 4):
        self._game_state: List[List[Tile]] = initial_state
        self._game_state_1: List[List[Tile]] = deepcopy(initial_state)
        self.occupied_tolerance = occupied_tolerance
        self.swapped: bool = False
        self.occupied: int = 0

    def _get_game_state(self) -> List[List[Tile]]:
        return self._game_state if not self.swapped else self._game_state_1

    def _get_alt_game_state(self) -> List[List[Tile]]:
        return self._game_state_1 if not self.swapped else self._game_state

    def swap(self) -> None:
        self.swapped = False if self.swapped else True

    def get_occupied_seen(self, tile: Tile) -> int:
        occupied = 0
        for i, j in tile.neighbours:
            if self._get_game_state()[i][j].value == "#":
                occupied += 1
        return occupied

    def simulate_one_step(self) -> int:
        changes = 0
        for i in range(len(self._get_alt_game_state())):
            for j in range(len(self._get_alt_game_state()[i])):
                if self._get_alt_game_state()[i][j].value == ".":
                    continue
                occupied_count = self.get_occupied_seen(self._get_game_state()[i][j])

                if self._get_game_state()[i][j].value == "#" and occupied_count >= self.occupied_tolerance:
                    self._get_alt_game_state()[i][j].value = "L"
                    changes += 1
                    self.occupied -= 1
                elif self._get_game_state()[i][j].value == "L" and occupied_count == 0:
                    self._get_alt_game_state()[i][j].value = "#"
                    changes += 1
                    self.occupied += 1
                else:
                    self._get_alt_game_state()[i][j].value = self._get_game_state()[i][j].value
        self.swap()
        return changes

    def simulate(self, print: bool = True) -> None:
        if print:
            self.print()
        while self.simulate_one_step() > 0:
            if print:
                self.print()

    def get_occupied(self) -> int:
        return self.occupied

    def print(self) -> None:
        print()
        for line in self._get_game_state():
            print("".join([tile.value for tile in line]))
        print()


with open("input") as f:
    textinput = [list(c.replace("\n", "")) for c in f.readlines()]

initial_game_state = []
for i, line in enumerate(textinput):
    state_line = []
    for j, char in enumerate(line):
        if char == ".":
            state_line.append(Tile(char, []))
            continue
        neighbours = [
            (i + x, j + y)
            for x, y in itertools.product(range(-1, 2), repeat=2)
            if (x != 0 or y != 0) and 0 <= i + x < len(textinput) and 0 <= j + y < len(line)
        ]
        state_line.append(Tile(char, neighbours))
    initial_game_state.append(state_line)

game = Game(initial_game_state)
game.simulate(print=True)
print("task 1:", game.get_occupied())

initial_game_state = []
for i, line in enumerate(textinput):
    state_line = []
    for j, char in enumerate(line):
        if char == ".":
            state_line.append(Tile(char, []))
            continue
        neighbours = [
            n
            for n in (
                next(((x, j) for x in range(i - 1, -1, -1) if textinput[x][j] != "."), None),
                next(((x, j) for x in range(i, len(textinput)) if x != i and textinput[x][j] != "."), None),
                next(((i, y) for y in range(j - 1, -1, -1) if textinput[i][y] != "."), None),
                next(((i, y) for y in range(j, len(textinput[i])) if y != j and textinput[i][y] != "."), None),
                next(((x, y) for x, y in zip(range(i - 1, -1, -1), range(j - 1, -1, -1)) if textinput[x][y] != "."), None),
                next(((x, y) for x, y in zip(range(i + 1, len(textinput)), range(j + 1, len(textinput[i]))) if textinput[x][y] != "."), None),
                next(((x, y) for x, y in zip(range(i - 1, -1, -1), range(j + 1, len(textinput[i]))) if textinput[x][y] != "."), None),
                next(((x, y) for x, y in zip(range(i + 1, len(textinput)), range(j - 1, -1, -1)) if textinput[x][y] != "."), None),
            )
            if n is not None
        ]
        state_line.append(Tile(char, neighbours))
    initial_game_state.append(state_line)
game = Game(initial_game_state, occupied_tolerance=5)
game.simulate(print=True)
print("task 2:", game.get_occupied())
