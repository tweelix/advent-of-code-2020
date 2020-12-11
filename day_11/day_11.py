from copy import deepcopy

class Game:
    def __init__(self, initial_state, occupied_tolerance=4, rule=1):
        self._game_state: list = initial_state
        self._game_state_1: list = deepcopy(initial_state)
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

    def _rule_1_get_occupied(self, i, j):
        occupied_neighbours = 0
        for x in range(-1, 2):
            for y in range(-1, 2):
                if (x != 0 or y != 0) and 0 <= i+x < len(self._get_game_state()) and 0 <= j+y < len(self._get_game_state()[i]):
                    if self._get_game_state()[i+x][j+y] == "#":
                        occupied_neighbours += 1
        return occupied_neighbours

    def _rule_2_get_occupied(self, i, j):
        occupied_neighbours = 0
        for x in range(i-1, -1, -1):
            # print(x,j)
            if self._get_game_state()[x][j] == "#":
                occupied_neighbours += 1
                break
            elif self._get_game_state()[x][j] == "L":
                break
        for x in range(i, len(self._get_game_state())):
            # print(x,j)
            if x != i:
                if self._get_game_state()[x][j] == "#":
                    occupied_neighbours += 1
                    break
                elif self._get_game_state()[x][j] == "L":
                    break
        for y in range(j-1, -1, -1):
            # print(i,y)
            if self._get_game_state()[i][y] == "#":
                occupied_neighbours += 1
                break
            elif self._get_game_state()[i][y] == "L":
                break
        for y in range(j, len(self._get_game_state()[i])):
            # print((i, j), (i,y))
            if y != j:
                if self._get_game_state()[i][y] == "#":
                    occupied_neighbours += 1
                    break
                elif self._get_game_state()[i][y] == "L":
                    break
        x = i-1
        y = j-1
        while (x >= 0 and y >= 0):
            # print(x,y)
            if self._get_game_state()[x][y] == "#":
                occupied_neighbours += 1
                break
            elif self._get_game_state()[x][y] == "L":
                break
            x -= 1
            y -= 1
        x = i+1
        y = j+1
        while (x < len(self._get_game_state()) and y < len(self._get_game_state()[i])):
            # print(x,y)
            if self._get_game_state()[x][y] == "#":
                occupied_neighbours += 1
                break
            elif self._get_game_state()[x][y] == "L":
                break
            x += 1
            y += 1
        x = i-1
        y = j+1
        while (x >= 0 and y < len(self._get_game_state()[i])):
            # print(x,y)
            if self._get_game_state()[x][y] == "#":
                occupied_neighbours += 1
                break
            elif self._get_game_state()[x][y] == "L":
                break
            x -= 1
            y += 1
        x = i+1
        y = j-1
        while (x < len(self._get_game_state()) and y >= 0):
            # print(x,y)
            if self._get_game_state()[x][y] == "#":
                occupied_neighbours += 1
                break
            elif self._get_game_state()[x][y] == "L":
                break
            x += 1
            y -= 1
        return occupied_neighbours

    def get_occupied_seen(self):
        if self.rule == 1:
            return self._rule_1_get_occupied
        if self.rule == 2:
            return self._rule_2_get_occupied

    def simulate_one_step(self):
        changes = 0
        for i in range(len(self._get_alt_game_state())):
            for j in range(len(self._get_alt_game_state()[i])):
                if self._get_alt_game_state()[i][j] == ".":
                    continue
                occupied_count = self.get_occupied_seen()(i, j)
                # print(occupied_count)

                if self._get_game_state()[i][j] == "#" and occupied_count >= self.occupied_tolerance:
                    self._get_alt_game_state()[i][j] = "L"
                    changes += 1
                    self.occupied -= 1
                elif self._get_game_state()[i][j] == "L" and occupied_count == 0:
                    self._get_alt_game_state()[i][j] = "#"
                    changes += 1
                    self.occupied += 1
                else:
                    self._get_alt_game_state()[i][j] = self._get_game_state()[i][j]
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
            print("".join([tile for tile in line]))
        print()


if __name__ == "__main__":
    initial_game_state = []
    with open("input") as f:
        textinput = [list(c.replace("\n", "")) for c in f.readlines()]
                   
    game = Game(deepcopy(textinput))
    game.simulate(print=True)
    print("task 1:", game.get_occupied())

    game = Game(deepcopy(textinput), occupied_tolerance=5, rule=2)
    game.simulate(print=True)
    # # game.print()
    print("task 2:", game.get_occupied())
