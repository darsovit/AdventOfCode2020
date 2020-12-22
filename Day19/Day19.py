#! python

import re

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))

def testInput():
    return ['0: 4 1 5', '1: 2 3 | 3 2', '2: 4 4 | 5 5', '3: 4 5 | 5 4', '4: "a"', '5: "b"',
            '',
            'ababbb',
            'bababa',
            'abbbab',
            'aaabbb',
            'aaaabbb']

class RuleGraph:
    def __init__(self):
        self.rules = {}
        self.evaluatedRules = {}
        self.literalRule = re.compile(r'^(?P<ruleno>\d+): "(?P<value>[a-z])"$')
        self.compositeRule = re.compile(r'^(?P<ruleno>\d+): (?P<value>[ \d\|]+)$')
        self.tokenifyCompositeValue = re.compile(r'(?P<subrule>\d+)|(?P<whitespace>\s)|(?P<divider>\|)')
        
    def ParseRule(self, line):
        match = self.literalRule.match(line)
        if match is not None:
            self.evaluatedRules[int(match['ruleno'])] = match['value']
            return True
        else:
            match = self.compositeRule.match(line)
            if match is not None:
                self.rules[int(match['ruleno'])] = match['value']
                return True
        return False

    def __tokenifyRule( self, ruleNo ):
        tokens = []
        done = False
        rule = self.rules[ruleNo]
        pos  = 0

        while not done:
            match = self.tokenifyCompositeValue.match( rule, pos )
            if match is not None:
                pos = match.end()
                if match.lastgroup != 'whitespace':
                    if match.lastgroup == 'subrule':
                        tokens += [('subrule',int(match[match.lastgroup]))]
                    else:
                        assert match.lastgroup == 'divider', match.lastgroup
                        tokens += [(match.lastgroup, match[match.lastgroup])]
            else:
                assert len(rule) == pos, '{}'.format(rule[pos:])
                done = True
        return tokens

    def EvaluateRules(self, ruleNo):
        if ruleNo in self.evaluatedRules:
            return self.evaluatedRules[ruleNo]
        else:
            value = ''
            divided = False
            tokens = self.__tokenifyRule( ruleNo )
            #print(tokens)
            for token in tokens:
                if token[0] == 'subrule':
                    value += self.EvaluateRules(token[1])
                elif token[0] == 'divider':
                    value += '|'
                    divided = True
            if divided:
                value = '(' + value + ')'
            self.evaluatedRules[ruleNo] = value
            return value

rulegraph = RuleGraph()
input = readInput()
buildingRules = True
ruleRegex = None
countMatches = 0
for line in input:
    if buildingRules:
        buildingRules = rulegraph.ParseRule(line)
        if not buildingRules:
            ruleRegex = r'^' + rulegraph.EvaluateRules(0) + r'$'
            ruleRe = re.compile(ruleRegex)
            #print(rulegraph.rules)
            #print(rulegraph.evaluatedRules)
            #print(ruleRegex)
    else:
        assert ruleRegex is not None, ruleRegex
        match = ruleRe.match(line)
        if match is not None:
            countMatches += 1
        #print('Test:',line, match is not None)
        
print(countMatches)