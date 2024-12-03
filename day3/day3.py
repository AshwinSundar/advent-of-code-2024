from enum import Enum

class TokenType(Enum):
    MUL = 0

class Parser:
    def __init__(self, fileName):
        # open file, read contents into buffer
        with open(fileName, 'r') as data:
            self.source = data.read()
            self.source_len = len(self.source)
        self.pos = 0
        self.sum = 0 # sum of all mul expressions
        self.currExpr = (None, None, None) # can be a tuple (mul, num1, num2)

    # increment pos by 1
    # if EOF, return answer and exit
    def advance(self):
        if self.is_end(self.pos):
            return(self.sum)
        else:
            self.pos += 1

    # get next token without advancing
    # if EOF, return None
    def peek(self):
        if self.is_end(self.pos):
            return None
        else:
            return self.source[self.pos + 1]

    # process token, accumulate
    def consume(self):
        match (self.currExpr):
            case (TokenType.MUL, a, b) if isinstance(a, int) and isinstance(b, int):
                self.sum += a * b
                self.discard()
            case _:
                print("unable to consume")
                self.sum += 0
                self.discard()

    # discard current expr and advance to next position
    def discard(self):
        self.currExpr = (None, None, None)
        self.advance()

    # 0-based index
    def is_end(self, pos):
        return pos + 1 >= self.source_len

    # give current context (i.e. matching chars that may produce a token)
    def parse(self, context):
        while not self.is_end(self.pos):
            match (self.currExpr):
                case (None, None, None):
                    match context:
                        case 'm' | 'mu' | 'mul':
                            self.advance()
                            context = context + self.source[self.pos]
                            continue

                        case 'mul(':
                            self.currExpr = (TokenType.MUL, None, None)
                            self.advance()
                            context = self.source[self.pos]
                            continue

                        case _:
                            self.discard()
                            if not self.is_end(self.pos):
                                context = self.source[self.pos]
                            continue

                case (TokenType.MUL, None, None):
                    match context:
                        case _ if context.isdigit():
                            self.advance()
                            context = context + self.source[self.pos]
                            continue

                        case _ if context.endswith(","):
                            self.currExpr = (self.currExpr[0], int(context[:-1]), self.currExpr[2])
                            self.advance()
                            context = self.source[self.pos]
                            continue

                        case _:
                            self.discard()
                            context = self.source[self.pos]
                            continue

                case (TokenType.MUL, int(), None):
                # case (TokenType.MUL, _, None):
                    match context:
                        case _ if context.isdigit():
                            self.advance()
                            context = context + self.source[self.pos]
                            continue

                        case _ if context.endswith(")"):
                            self.currExpr = (self.currExpr[0], self.currExpr[1], int(context[:-1]))
                            self.consume()
                            context = self.source[self.pos]
                            continue

                        case _:
                            self.discard()
                            context = self.source[self.pos]
                            continue

        return self.sum

# parser = Parser("day3-input1.txt")
parser = Parser("day3-input2.txt")
print(parser.parse(""))
