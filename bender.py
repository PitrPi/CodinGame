import pandas as pandas
import sys


class Game:
    def __init__(self, x, y, plan, teleports):
        self._plan = plan
        self._teleports = teleports
        self.x = x
        self.y = y
        self._directions = ["SOUTH", "EAST", "NORTH", "WEST"]
        self._diridx = 0
        self.direction = self._directions[self._diridx]
        self.out = []
        self._breaker = False
        self._inverter = False
        self._states = []

    def dir_map(self):
        if self.direction == "SOUTH":
            return self.x + 1, self.y
        elif self.direction == "EAST":
            return self.x, self.y + 1
        elif self.direction == "NORTH":
            return self.x - 1, self.y
        elif self.direction == "WEST":
            return self.x, self.y - 1

    def look_ahead(self):
        x, y = self.dir_map()
        if self._plan[x][y] == "#" or (self._plan[x][y] == "X" and not self._breaker):
            return False
        else:
            return True

    def change_direction(self, direction=None):
        if direction is None:
            if self._inverter:
                self._diridx = (self._diridx-1) % 4
            else:
                self._diridx = (self._diridx+1) % 4
        else:
            if direction == "S" or direction == "SOUTH":
                self._diridx = 0
            elif direction == "E" or direction == "EAST":
                self._diridx = 1
            elif direction == "N" or direction == "NORTH":
                self._diridx = 2
            elif direction == "W" or direction == "WEST":
                self._diridx = 3
        self.direction = self._directions[self._diridx]

    def step(self):
        # turn left approach
        # while not self.look_ahead():
        #     self.change_direction()
        for d in {False: "SENW", True: "WNES"}[self._inverter]:
            if self.look_ahead():
                break
            self.change_direction(d)
        self.out.append(self.direction)
        self.x, self.y = self.dir_map()
        stand = self._plan[self.x][self.y]
        if stand in "SENW":
            self.change_direction(direction=stand)
        elif stand == "X":
            # self._breaker = False
            self._plan[self.x][self.y] = " "
            self._states = []  # Reset visited states
        elif stand == "B":
            self._breaker = not self._breaker
        elif stand == "I":
            self._inverter = not self._inverter
        elif stand == "T":
            if self._teleports[0] == [self.x, self.y]:
                self.x, self.y = self._teleports[1]
            else:
                self.x, self.y = self._teleports[0]
        elif stand == "$":
            return False
        # Loop check
        if [self.x, self.y, self._breaker, self._inverter, self.direction] in self._states:
            self.out = ["LOOP"]
            return False
        else:
            self._states.append([self.x, self.y, self._breaker, self._inverter, self.direction])
            return True


if __name__ == '__main__':

    if False:   # Codingame input
        plan = {}
        x, y = 0, 0
        teleports = []

        # Init
        l, _ = [int(i) for i in input().split()]
        for i in range(l):
            row = input()
            # Find Bender
            bender = row.find("@")
            if bender != -1:
                x, y = i, bender
            # Find Teleport
            teleport = row.find("T")
            if teleport != -1:
                teleports.append([i, teleport])
                teleport = row.find("T", teleport+1)
                if teleport != -1:
                    teleports.append([i, teleport])
            # Parse to dict/list map
            plan[i] = [ch for ch in row]
        plan[x][y] = " "
    else:  # Manual input
        plan = {0: ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'], 1: ['#', ' ', '@', ' ', ' ', ' ', ' ', ' ', ' ', '#'], 2: ['#', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', '#'], 3: ['#', 'X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', '#'], 4: ['#', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', '#'], 5: ['#', ' ', ' ', ' ', ' ', 'B', 'X', 'X', '$', '#'], 6: ['#', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '#'], 7: ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'], 8: ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'], 9: ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#']}
        df = pandas.DataFrame.from_dict(plan, orient="index")
        x, y = (1, 2)
        teleports = []

    looping = True
    g = Game(x, y, plan, teleports)
    while looping:
        looping = g.step()
        df = pandas.DataFrame.from_dict(g._plan, orient="index")
        df.iloc[g.x, g.y] = "@"

    for ins in g.out:
        print(ins)
