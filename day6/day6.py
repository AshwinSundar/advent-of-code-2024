from enum import Enum
from typing import List
import numpy as np

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

def addPoints(a: Point, b: Point):
    return Point(a.x + b.x, a.y + b.y)



class Direction(Enum):
    UP = Point(0,-1)
    RIGHT = Point(1,0)
    DOWN = Point(0,1)
    LEFT = Point(-1,0)

class Guard:
    def __init__(self, fileName, startChar):
        with open(fileName, 'r') as data:
            self.source = data.read()
            self.matrix = self.convertToMatrix(self.source)

        self.pos: Point = self.findFirstChar(startChar)
        self.maxX = len(self.matrix[0]) - 1
        self.maxY = len(self.matrix) - 1
        self.path: List[Point] = [self.pos]
        match startChar:
            case "^":
                self.direction = Direction.UP
            case ">": 
                self.direction = Direction.RIGHT
            case "<":
                self.direction = Direction.LEFT
            case "v":
                self.direction = Direction.DOWN

    def convertToMatrix(self, input):
        return np.array([list(line) for line in input.strip().split('\n')])

    def findFirstChar(self, char):
        for line_index, line in enumerate(self.matrix):
            for char_index, char_val in enumerate(line):
                if char == char_val:
                    return Point(char_index, line_index)
        raise Exception("startChar ", char, " not found.")

    def walk(self):
        if self.pos not in self.path:
            self.path.append(self.pos)

    def moveNext(self):
        nextPt = addPoints(self.pos, self.direction.value)
        if (nextPt.x > self.maxX 
            or nextPt.x < 0 
            or nextPt.y > self.maxY 
            or nextPt.y < 0):
            return False

        next = self.matrix[nextPt.y][nextPt.x]

        if next == "#":
            self.turnRight()
            nextPt = addPoints(self.pos, self.direction.value)
            self.pos = nextPt
        else:
            self.pos = nextPt

        self.walk()
        return True

    def findEnd(self):
        while (self.moveNext()):
            continue

    def turnRight(self):
        match self.direction:
            case Direction.UP:
                self.direction = Direction.RIGHT
            case Direction.RIGHT: 
                self.direction = Direction.DOWN
            case Direction.DOWN:
                self.direction = Direction.LEFT
            case Direction.LEFT:
                self.direction = Direction.UP

    def findStart(self, startChar):
        self.pos = self.findFirstChar(startChar)

guard = Guard("input.txt", "^")
guard.findEnd()
print(len(guard.path))
