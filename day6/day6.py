from enum import Enum
import numpy as np

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, p: 'Point'):
        self.x += p.x
        self.y += p.y

class Move(Enum):
    UP = Point(0,-1)
    RIGHT = Point(1,0)
    DOWN = Point(0,1)
    LEFT = Point(-1,0)

class Guard:
    def __init__(self, fileName, startChar):
        with open(fileName, 'r') as data:
            self.source = data.read()
            self.matrix = self.convertToMatrix(self.source)

        self.pos = self.findFirstChar(startChar)
        self.totalDistance = 0

    def convertToMatrix(self, input):
        return np.array([list(line) for line in input.strip().split('\n')])

    def findFirstChar(self, char):
        for line_index, line in enumerate(self.matrix):
            for char_index, char_val in enumerate(line):
                if char == char_val:
                    return (line_index, char_index)
        return None

    # how far to traverse before reaching endChar
    # if endChar is not found, must have exceeded bounds - return totalDistance
    def findLineEnd(self, endChar):
        sum = 0
            # self.pos += 
        pass

    
    # YOU ARE HERE - you need to keep track of the direction the Guard is facing first, before you can implement this. May need to refactor findStart a bit
    def turnRight(self):

    def findStart(self, startChar):
        self.pos = findFirstChar(startChar)
        match startChar:
            case "^":
                self.direction = Move.UP
            case ">": 
                self.direction = Move.RIGHT
            case "<":
                self.direction = Move.LEFT
            case "v":
                self.direction =  Move.DOWN


guard = Guard("input.txt", "^")
print(guard.pos)
