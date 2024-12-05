class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Parser:
    def __init__(self, fileName):
        self.xmasCount = 0
        self.pos = Point(0, 0)

        with open(fileName, 'r') as data:
            self.source = data.read()
            self.matrix = self.source.splitlines()
            self.maxX = len(self.matrix[0])
            self.maxY = len(self.matrix)

    def checkXMAS(self, y, x):
        directions = [
            [(0,0), (0,1), (0,2), (0,3)],  # right
            [(0, 0), (-1, 0), (-2, 0), (-3, 0)], # left
            [(0, 0), (0, -1), (0, -2), (0, -3)], # up
            [(0,0), (1,0), (2,0), (3,0)],  # down
            [(0,0), (-1,1), (-2,2), (-3,3)],  # diagonal down-left
            [(0,0), (1,1), (2,2), (3,3)],  # diagonal down-right
            [(0, 0), (-1, -1), (-2, -2), (-3, -3)], # diagonal up-left
            [(0, 0), (1, -1), (2, -2), (3, -3)]# diagonal up-right
        ]

        count = 0
        for dir in directions:
            if all(y+dy < len(self.matrix) and x+dx < len(self.matrix[0]) and 
                  y+dy >= 0 and x+dx >= 0 and
                  self.matrix[y+dy][x+dx] == "XMAS"[i] 
                  for i, (dy,dx) in enumerate(dir)):
                count += 1
        return count
        

    def countXmases(self):
        total = 0
        for y in range(self.maxY):
            for x in range(self.maxX):
                if self.matrix[y][x] == 'X':
                    total += self.checkXMAS(y, x)
        return total


    def checkXMAS2(self, y, x):
        count = 0

        # First check if all required positions are within bounds
        if (y+1 >= self.maxY or y-1 < 0 or 
            x+1 >= self.maxX or x-1 < 0):
            return count

        # Config 1: M in bottom-right, S in bottom-left
        if (self.matrix[y+1][x+1] == "M" and 
            self.matrix[y+1][x-1] == "S" and 
            self.matrix[y-1][x+1] == "M" and 
            self.matrix[y-1][x-1] == "S"):
            count += 1

        # Config 2: S in bottom-right, M in bottom-left
        if (self.matrix[y+1][x+1] == "S" and 
            self.matrix[y+1][x-1] == "M" and 
            self.matrix[y-1][x+1] == "S" and 
            self.matrix[y-1][x-1] == "M"):
            count += 1

        # Config 3: M in bottom-right, M in bottom-left
        if (self.matrix[y+1][x+1] == "M" and 
            self.matrix[y+1][x-1] == "M" and 
            self.matrix[y-1][x+1] == "S" and 
            self.matrix[y-1][x-1] == "S"):
            count += 1

        # Config 4: S in bottom-right, S in bottom-left
        if (self.matrix[y+1][x+1] == "S" and 
            self.matrix[y+1][x-1] == "S" and 
            self.matrix[y-1][x+1] == "M" and 
            self.matrix[y-1][x-1] == "M"):
            count += 1

        return count

    def countXmases2(self):
        total = 0
        for y in range(self.maxY):
            for x in range(self.maxX):
                if self.matrix[y][x] == "A":
                    total += self.checkXMAS2(y,x)

        return total


parser = Parser("day4-input.txt")
print(parser.countXmases())
print(parser.countXmases2())



