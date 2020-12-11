from copy import deepcopy
from functools import reduce
from typing import List, Tuple


class Tile:
    def __init__(self, value, neighbours):
        self.value: str = value
        self.neighbours: List[Tuple[int, int]] = neighbours


class Game:
    def __init__(self, initial_state, occupied_tolerance=4, rule=1):
        self._game_state: List[Tile] = initial_state
        self._game_state_1: List[Tile] = deepcopy(initial_state)
        self.swapped: bool = False
        self.occupied = 0
        self.occupied_tolerance = occupied_tolerance
        self.rule = rule

    def _get_game_state(self):
        return self._game_state if not self.swapped else self._game_state_1

    def _get_alt_game_state(self):
        return self._game_state_1 if not self.swapped else self._game_state

    def swap(self):
        self.swapped = False if self.swapped else True

    def get_occupied_seen(self, tile: Tile):
        occupied = 0
        for i, j in tile.neighbours:
            if self._get_game_state()[i][j].value == "#":
                occupied += 1
        return occupied

    def simulate_one_step(self):
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

    def simulate(self, print=True):
        if print:
            self.print()
        while(self.simulate_one_step() > 0):
            if print:
                self.print()

    def get_occupied(self):
        return self.occupied

    def print(self):
        print()
        for line in self._get_game_state():
            print("".join([tile.value for tile in line]))
        print()


if __name__ == "__main__":
    initial_game_state = []
    with open("input") as f:
        textinput = [list(c.replace("\n", "")) for c in f.readlines()]

    initial_game_state = []
    for i, line in enumerate(textinput):
        state_line = []
        for j, char in enumerate(line):
            neighbours = []
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if (x != 0 or y != 0) and 0 <= i+x < len(textinput) and 0 <= j+y < len(line):
                        neighbours.append((i+x, j+y))
            state_line.append(Tile(char, neighbours))
        initial_game_state.append(state_line)
        
    game = Game(deepcopy(initial_game_state))
    game.simulate(print=True)
    print("task 1:", game.get_occupied())

    initial_game_state = []

    initial_game_state = []
    for i, line in enumerate(textinput):
        state_line = []
        for j, char in enumerate(line):
            neighbours = []
            if char == ".":
                state_line.append(Tile(char, []))
                continue
            for x in range(i-1, -1, -1):
                if textinput[x][j] != ".":
                    neighbours.append((x,j))
                    break
            for x in range(i, len(textinput)):
                if x != i:
                    if textinput[x][j] != ".":
                        neighbours.append((x,j))
                        break
            for y in range(j-1, -1, -1):
                if textinput[i][y] != ".":
                    neighbours.append((i,y))
                    break
            for y in range(j, len(textinput[i])):
                if y != j:
                    if textinput[i][y] != ".":
                        neighbours.append((i,y))
                        break
            x = i-1
            y = j-1
            while (x >= 0 and y >= 0):
                if textinput[x][y] != ".":
                    neighbours.append((x,y))
                    break
                x -= 1
                y -= 1
            x = i+1
            y = j+1
            while (x < len(textinput) and y < len(textinput[i])):
                if textinput[x][y] != ".":
                    neighbours.append((x,y))
                    break
                x += 1
                y += 1
            x = i-1
            y = j+1
            while (x >= 0 and y < len(textinput[i])):
                if textinput[x][y] != ".":
                    neighbours.append((x,y))
                    break
                x -= 1
                y += 1
            x = i+1
            y = j-1
            while (x < len(textinput) and y >= 0):
                if textinput[x][y] != ".":
                    neighbours.append((x,y))
                    break
                x += 1
                y -= 1
            state_line.append(Tile(char, neighbours))
            # print((i, j), neighbours)
        initial_game_state.append(state_line)
    game = Game(deepcopy(initial_game_state), occupied_tolerance=5)
    game.simulate(print=True)
    print("task 2:", game.get_occupied())
