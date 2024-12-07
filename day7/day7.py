from itertools import product

def getAnswer(line):
    return int(line.split(":")[0])

def getOperands(line):
    return [int(x) for x in line.split(" ")[1:]]

def getSource(fileName):
    with open(fileName) as f:
        return f.read()

def evaluateLeftToRight(operands, operators):
    result = operands[0]
    for i, op in enumerate(operators):
        if op == '+':
            result += operands[i + 1]
        elif op == '*':
            result *= operands[i + 1]
        elif op == "||":
            result = int(str(result) + str(operands[i + 1]))
    return result

def tryCombinations(operands, ans):
    operators = ['+', '*', "||"]
    allCombinations = product(operators, repeat=len(operands) - 1)

    for ops in allCombinations:
        result = evaluateLeftToRight(operands, ops)
        if result == ans:
            return True
    return False

source = getSource("input.txt").splitlines()
sum = 0

for line in source:
    ans = getAnswer(line)
    operands = getOperands(line)

    if tryCombinations(operands, ans):
        sum += ans

print(sum)
