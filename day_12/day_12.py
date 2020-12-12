import numpy as np


class Rotations:
    r_90 = np.array([[0, -1], [1, 0]])
    r_180 = np.array([[-1, 0], [0, -1]])
    r_270 = -   r_90
    rotations_lut = {90: r_90, 180: r_180, 270: r_270}
    rotation_direction_lut = {"L": 1, "R": -1}


class Movements:
    movements = {
        "N": np.array([0, 1]),
        "S": np.array([0, -1]),
        "E": np.array([1, 0]),
        "W": np.array([-1, 0]),
    }


class Ship:
    def __init__(self):
        self.position = np.array([0, 0])
        self.direction = np.array([1, 0])

    def handle_command(self, command, value):
        if command in Movements.movements.keys():
            self.move(command, value)
        elif command in Rotations.rotation_direction_lut.keys():
            self.turn(command, value)
        elif command == "F":
            self.forward(value)

    def forward(self, distance):
        self.position += distance * self.direction

    def turn(self, direction, angle):
        sign = 1 if angle == 180 else Rotations.rotation_direction_lut[direction]
        rotation = Rotations.rotations_lut[angle]
        self.direction = (sign * rotation).dot(self.direction)

    def move(self, direction, distance):
        self.position += Movements.movements[direction] * distance


class ShipWithBeacon:
    def __init__(self):
        self.beacon_position = np.array([10, 1])
        self.ship_position = np.array([0, 0])

    def handle_command(self, command, value):
        if command in Movements.movements.keys():
            self.move(command, value)
        elif command in Rotations.rotation_direction_lut.keys():
            self.turn(command, value)
        elif command == "F":
            self.forward(value)

    def forward(self, distance):
        self.ship_position += self.beacon_position * distance

    def turn(self, direction, angle):
        sign = 1 if angle == 180 else Rotations.rotation_direction_lut[direction]
        rotation = Rotations.rotations_lut[angle]
        self.beacon_position = (sign * rotation).dot(self.beacon_position)

    def move(self, direction, distance):
        self.beacon_position += Movements.movements[direction] * distance


with open("input") as f:
    input = [(i[:1], int(i[1:])) for i in f.readlines()]

ship = Ship()
for direction, distance in input:
    ship.handle_command(direction, distance)
print("Task 1:", np.sum(np.absolute(ship.position)))

ship = ShipWithBeacon()
for direction, distance in input:
    ship.handle_command(direction, distance)
print("Task 2:", np.sum(np.absolute(ship.ship_position)))
