from enum import IntEnum
from typing import List, Union
from functools import reduce


class FileSystem:
    def __init__(self, fileName):
        with open(fileName, 'r') as data:
            self.diskMap = data.read().rstrip()

        self.blockMap = self.getBlockMap()
        self.compactBlockMap1 = self.getCompactBlockMap1()
        self.compactBlockMap2 = self.getCompactBlockMap2()

    def getBlockMap(self):
        blockMap = []
        for idx, char in enumerate(self.diskMap):
            if idx % 2 == 0:
                for _ in range(int(char)):
                    blockMap.append(int(idx/2))
            elif idx %2 != 0:
                for _ in range(int(char)):
                    blockMap.append('.')
        return blockMap

    def getCompactBlockMap1(self):
        blockMap = self.blockMap

        for idx_b, char_b in enumerate(blockMap[:len(blockMap) - 1]):
            if char_b == ".":
                revBlockMap = list(reversed(blockMap))
                for idx_r, char_r in enumerate(revBlockMap):
                    if char_r != ".":
                        blockMap[idx_b] = char_r
                        blockMap[len(blockMap) - idx_r - 1] = "."
                        break

        return list(filter(lambda c: c != ".", blockMap))

    def getCheckSum(self, lst):
        sum = 0
        for idx, char in enumerate(lst):
            if isinstance(char, int):
                sum += idx * int(char)
        return sum

    # YOU ARE HERE - this is still wrong
    # you need to skip ahead in the for loop after encountering a block, instead of just going to the next char
    # convert the block map into chunks based on common contiguous chars, then reprocess
    # 1) getChunkedBlockMap
    # 2) for each_r in reverseChunkedBlockMap, for each_c in chunkedBlockMap, if len(each_c) <= len(each_r), replace ...
    def getCompactBlockMap2(self):
        blockMap = self.blockMap
        revBlockMap = list(reversed(blockMap))

        for idx_r, char_r in enumerate(revBlockMap):
            if char_r != ".":
                fileLen = self.countContiguousChars(char_r, idx_r, revBlockMap)

                for idx_b, char_b in enumerate(blockMap[:len(blockMap) - 1]):
                    if char_b == ".":
                        freeLen = self.countContiguousChars(".", idx_b, blockMap)
                        
                        if fileLen <= freeLen:
                            blockMap[idx_b:idx_b + fileLen] = [char_r]*fileLen
                            blockMap[len(blockMap) - idx_r - 1:len(blockMap) - idx_r - fileLen - 1] = ['.'] * fileLen

        return blockMap

    def countContiguousChars(self, char, start, lst):
        count = 0
        idx = start
        next = lst[idx]

        while next == char and idx < len(lst) - 1:
            count += 1
            idx += 1
            next = lst[idx]

        return count

fs = FileSystem("example.txt")
print(fs.compactBlockMap2)
print(fs.getCheckSum(fs.compactBlockMap2))
