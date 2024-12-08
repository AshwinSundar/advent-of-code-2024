from typing import List

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Position(self.x - other.x, self.y - other.y)

class Antenna:
    def __init__(self, freq: str, position: Position):
        self.freq = freq
        self.pos = position

    def __repr__(self):
        return f"({self.freq}, {self.pos})"


class AntennaMap:
    def __init__(self, fileName):
        with open(fileName, "r") as data:
            self.source = data.read().splitlines()
            self.frequencies = self.getFrequencies(self.source, ['.'])
            self.antennae: List[Antenna] = self.findAllAntennae(self.source, self.frequencies)
            self.antennaPairs = self.getAntennaPairs(self.antennae)
            self.maxX = len(self.source[0]) - 1
            self.maxY = len(self.source) - 1

    def getFrequencies(self, matrix, exclude: List[str]):
        frequencies = []
        for line in matrix:
            for char in line:
                if char not in exclude and char not in frequencies:
                    frequencies.append(char)
        
        return frequencies

    def findAllAntennae(self, matrix, freqList):
        antennae: List[Antenna] = []
        for yIndex, line in enumerate(matrix):
            for xIndex, char in enumerate(line):
                if char in freqList:
                    antennae.append(Antenna(char, Position(xIndex, yIndex)))

        return antennae

    def getAntennaPairs(self, antennae):
        antennaPairs = []
        for idx, ant1 in enumerate(antennae):
            for ant2 in antennae[idx+1:]:
                if ant1.freq == ant2.freq and (ant1, ant2) not in antennaPairs:
                    antennaPairs.append((ant1, ant2))

        return antennaPairs

    def isInBounds(self, pt: Position):
        return (pt.x >= 0 and
                pt.x <= self.maxX and
                pt.y >= 0 and
                pt.y <= self.maxY)

    def countAntinodes1(self):
        antinodes = []
        for pair in self.antennaPairs:
            diff = Position(abs(pair[0].pos.x - pair[1].pos.x), abs(pair[0].pos.y - pair[1].pos.y))

            antinode1 = Position(0, 0)
            antinode2 = Position(0, 0)

            # set antinode1.x
            if (pair[0].pos.x >= pair[1].pos.x):
                antinode1.x = pair[0].pos.x + diff.x
            else: 
                antinode1.x = pair[0].pos.x - diff.x

            # set antinode1.y
            if (pair[0].pos.y >= pair[1].pos.y):
                antinode1.y = pair[0].pos.y + diff.y
            else:
                antinode1.y = pair[0].pos.y - diff.y

            # set antinode2.x
            if (pair[1].pos.x >= pair[0].pos.x):
                antinode2.x = pair[1].pos.x + diff.x
            else: 
                antinode2.x = pair[1].pos.x - diff.x

            # set antinode2.y
            if (pair[1].pos.y >= pair[0].pos.y):
                antinode2.y = pair[1].pos.y + diff.y
            else:
                antinode2.y = pair[1].pos.y - diff.y

            if self.isInBounds(antinode1) and antinode1 not in antinodes:
                antinodes.append(antinode1)

            if self.isInBounds(antinode2) and antinode2 not in antinodes:
                antinodes.append(antinode2)

        return len(antinodes)

    def countAntinodes2(self):
        antinodes = []
        for pair in self.antennaPairs:
            slope = Position(pair[0].pos.x - pair[1].pos.x, pair[0].pos.y - pair[1].pos.y)
            next = pair[0].pos + slope

            while self.isInBounds(next):
                if next not in antinodes:
                    antinodes.append(next)
                next += slope

            next -= slope

            while self.isInBounds(next):
                if next not in antinodes:
                    antinodes.append(next)
                next -= slope

        return len(antinodes)


am = AntennaMap("input.txt")
print(f"Part 1: {am.countAntinodes1()}")
print(f"Part 2: {am.countAntinodes2()}")
