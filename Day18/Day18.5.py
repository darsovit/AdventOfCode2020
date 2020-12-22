#! python

import re
def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))

token_pattern = r"""
(?P<literal>\d+)
|(?P<openparen>\()
|(?P<closeparen>\))
|(?P<addition>\+)
|(?P<multiply>\*)
|(?P<whitespace>\s+)
"""
token_re = re.compile(token_pattern, re.VERBOSE)

def tokenize(line):
    pos = 0
    done = False
    while not done:
        m = token_re.match(line, pos)
        if m is not None:
            pos = m.end()
            if m.lastgroup != 'whitespace':
                if m.lastgroup == 'literal':
                    yield (m.lastgroup, int(m[m.lastgroup]))
                else:
                    yield (m.lastgroup, m[m.lastgroup])
        else:
            assert len(line) == pos, '{}'.format(line[pos:])
            done = True
    if pos != len(line):
        print('Failed to tokenize full line')

STATE_INIT_VALUE = 0
STATE_NEED_OP = 1
STATE_NEED_OPERAND_VALUE = 2

class Evaluate:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos    = 0


    def __performAllLiteralAdditions(self):
        for i in range(len(self.tokens)-1,0,-1):
            if self.tokens[i][0] == 'addition':
                if self.tokens[i-1][0] == 'literal' and self.tokens[i+1][0] == 'literal':
                    newliteral = ( 'literal', self.tokens[i-1][1] + self.tokens[i+1][1] )
                    self.tokens = self.tokens[:i-1] + [ newliteral ] + self.tokens[i+2:]

    def __performAllLiteralMultiplications(self):
        for i in range(len(self.tokens)-1,0,-1):
            if self.tokens[i][0] == 'multiply':
                if self.tokens[i-1][0] == 'literal' and self.tokens[i+1][0] == 'literal':
                    newliteral = ( 'literal', self.tokens[i-1][1] * self.tokens[i+1][1] )
                    self.tokens = self.tokens[:i-1] + [ newliteral ] + self.tokens[i+2:]

    def __evaluateParens(self):
        endparens = None
        startparens = None
        count = 0
        for i in range(len(self.tokens)-1,-1,-1):
            #print(count, self.tokens[i])
            if self.tokens[i][0] == 'closeparen':
                if endparens is None:
                    endparens = i
                count += 1

            elif self.tokens[i][0] == 'openparen':
                count -= 1
                if count == 0:
                    startparens = i
            #print( count, endparens, startparens )
            if count == 0 and endparens is not None and startparens is not None:
                innerEvaluate = Evaluate( self.tokens[startparens+1:endparens] )
                newliteral = ('literal', innerEvaluate.Evaluate())
                #print(self.tokens)
                self.tokens = self.tokens[:startparens] + [ newliteral ] + self.tokens[endparens+1:]
                #print(self.tokens)
                endparens = None
                startparens = None

    def Evaluate(self):
        value = 0
        self.__evaluateParens()
        self.__performAllLiteralAdditions()
        self.__performAllLiteralMultiplications()
        
        assert self.tokens[0][0] == 'literal', self.tokens
        return self.tokens[0][1]


def evaluateLine( line ):
    tokens = []
    for token in tokenize(line):
        tokens += [ token ]
    eval = Evaluate( tokens )
    return eval.Evaluate()

def AssertTestEvaluate( line, expected_value ):
    calculated_value = evaluateLine( line )
    assert calculated_value == expected_value, '{}; Expected: {}, Calculated: {}'.format(line, expected_value, calculated_value)
        
AssertTestEvaluate( '1 + 2 * 3 + 4 * 5 + 6', 231)
AssertTestEvaluate( '1 + (2 * 3) + (4 * (5 + 6))', 51)
AssertTestEvaluate( '2 * 3 + (4 * 5)', 46)
AssertTestEvaluate( '5 + (8 * 3 + 9 + 3 * 4 * 3)', 1445 )
AssertTestEvaluate( '5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', 669060 )
AssertTestEvaluate( '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 23340 )

value = 0
for line in readInput():
    value += evaluateLine( line )
print(value)
