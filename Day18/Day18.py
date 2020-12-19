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
        
    def takeToken(self):
        oldpos = self.pos
        self.pos += 1
        if len(self.tokens) > oldpos:
            return self.tokens[oldpos]
        else:
            return None

    def __evaluate(self, parenstarted=False):
        done = False
        state = STATE_INIT_VALUE
        value = 0
        stored_op = None
        ops = {'multiply': lambda x,y: x*y, 'addition': lambda x,y: x+y}

        token = self.takeToken()
        if state == STATE_INIT_VALUE:
            if token[0] == 'literal':
                value = int(token[1])
            elif token[0] == 'openparen':
                value = self.__evaluate(parenstarted=True)
            else:
                assert False, 'Invalid token in initial state: {}'.format( token )
            state = STATE_NEED_OP
        token = self.takeToken()
        while token is not None:
            if state == STATE_NEED_OP:
                if token[0] in ('multiply', 'addition'):
                    stored_op = token[0]
                elif token[0] in 'closeparen':
                    assert parenstarted, 'Close paren without open paren'
                    return value
                else:
                    assert False, 'Invalid token in need_op state: {}'.format( token )
                state = STATE_NEED_OPERAND_VALUE
            elif state == STATE_NEED_OPERAND_VALUE:
                if token[0] == 'literal':
                    newvalue = int(token[1])
                elif token[0] == 'openparen':
                    newvalue = self.__evaluate(parenstarted=True)                
                if newvalue is not None:
                    if stored_op in ops:
                        value = ops[stored_op](value, newvalue)
                    else:
                        assert False, 'Invalid stored_op with in need operand state: {}, {}'.format(stored_op)
                state = STATE_NEED_OP
            token = self.takeToken()    
        return value

    def Evaluate(self):
        return self.__evaluate()

def evaluateLine( line ):
    tokens = []
    for token in tokenize(line):
        tokens += [ token ]
    eval = Evaluate( tokens )
    return eval.Evaluate()

def AssertTestEvaluate( line, expected_value ):
    calculated_value = evaluateLine( line )
    assert calculated_value == expected_value, '{}; Expected: {}, Calculated: {}'.format(line, expected_value, calculated_value)
        
AssertTestEvaluate( '1 + 2 * 3 + 4 * 5 + 6', 71)
AssertTestEvaluate( '1 + (2 * 3) + (4 * (5 + 6))', 51)
AssertTestEvaluate( '2 * 3 + (4 * 5)', 26)
AssertTestEvaluate( '5 + (8 * 3 + 9 + 3 * 4 * 3)', 437 )
AssertTestEvaluate( '((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', 13632 )

value = 0
for line in readInput():
    value += evaluateLine( line )
print(value)
