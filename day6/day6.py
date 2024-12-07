from enum import Enum
from typing import List, Set, Tuple
import numpy as np
from copy import deepcopy

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
        self.startPos = self.pos  # Store starting position
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
        self.startDirection = self.direction  # Store starting direction


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

    def checkForLoop(self) -> bool:
        visited = set()
        positions = []
        self.pos = self.startPos
        self.direction = self.startDirection
        steps = 0
        max_steps = 1000  # Large enough to handle the input size

        while steps < max_steps:
            pos = (self.pos.x, self.pos.y)
            positions.append(pos)

            # If we've seen this position before, check for a loop
            if pos in visited:
                # Find all occurrences of this position
                indices = [i for i, p in enumerate(positions) if p == pos]
                for start_idx in indices[:-1]:  # Check all previous occurrences
                    loop = positions[start_idx:]
                    # If we have a loop with at least 2 unique positions
                    if len(set(loop)) > 1:
                        return True

            visited.add(pos)

            nextPt = addPoints(self.pos, self.direction.value)
            if (nextPt.x > self.maxX or nextPt.x < 0 or 
                nextPt.y > self.maxY or nextPt.y < 0):
                return False

            next = self.matrix[nextPt.y][nextPt.x]
            if next == "#":
                self.turnRight()
                nextPt = addPoints(self.pos, self.direction.value)
                self.pos = nextPt
            else:
                self.pos = nextPt

            steps += 1

        return False  # No loop found within max_steps

    def findValidObstructions(self) -> List[Point]:
        valid_positions = []
        original_matrix = deepcopy(self.matrix)

        for y in range(len(self.matrix)):
            for x in range(len(self.matrix[0])):
                if original_matrix[y][x] == "." and Point(x, y) != self.startPos:
                    # Try placing obstruction
                    self.matrix = deepcopy(original_matrix)
                    self.matrix[y][x] = "#"

                    # Check if it creates a loop
                    if self.checkForLoop():
                        valid_positions.append(Point(x, y))
                        #print(f"Found valid position at {x}, {y}")  # Debug print

        # Restore original state
        self.matrix = original_matrix
        self.pos = self.startPos
        self.direction = self.startDirection

        return valid_positions
    
# Part 1
guard = Guard("input.txt", "^")
guard.findEnd()
print(f"Part 1: {len(guard.path)}")

# Part 2 - this didn't end up being correct...
guard = Guard("input.txt", "^")
valid_positions = guard.findValidObstructions()
print(f"Part 2: {len(valid_positions)}")
