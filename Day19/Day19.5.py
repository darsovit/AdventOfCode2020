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

def testInput2():
    return [
        '42: 9 14 | 10 1',
        '9: 14 27 | 1 26',
        '10: 23 14 | 28 1',
        '1: "a"',
        '11: 42 31',
        '5: 1 14 | 15 1',
        '19: 14 1 | 14 14',
        '12: 24 14 | 19 1',
        '16: 15 1 | 14 14',
        '31: 14 17 | 1 13',
        '6: 14 14 | 1 14',
        '2: 1 24 | 14 4',
        '0: 8 11',
        '13: 14 3 | 1 12',
        '15: 1 | 14',
        '17: 14 2 | 1 7',
        '23: 25 1 | 22 14',
        '28: 16 1',
        '4: 1 1',
        '20: 14 14 | 1 15',
        '3: 5 14 | 16 1',
        '27: 1 6 | 14 18',
        '14: "b"',
        '21: 14 1 | 1 14',
        '25: 1 1 | 1 14',
        '22: 14 14',
        '8: 42',
        '26: 14 22 | 1 20',
        '18: 15 15',
        '7: 14 5 | 1 21',
        '24: 14 1',
        '',
        'abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa',
        'bbabbbbaabaabba',
        'babbbbaabbbbbabbbbbbaabaaabaaa',
        'aaabbbbbbaaaabaababaabababbabaaabbababababaaa',
        'bbbbbbbaaaabbbbaaabbabaaa',
        'bbbababbbbaaaaaaaabbababaaababaabab',
        'ababaaaaaabaaab',
        'ababaaaaabbbaba',
        'baabbaaaabbaaaababbaababb',
        'abbbbabbbbaaaababbbbbbaaaababb',
        'aaaaabbaabaaaaababaa',
        'aaaabbaaaabbaaa',
        'aaaabbaabbaaaaaaabbbabbbaaabbaabaaa',
        'babaaabbbaaabaababbaabababaaab',
        'aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba',
]

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
                value = '(?:' + value + ')'
            self.evaluatedRules[ruleNo] = value
            return value

rulegraph = RuleGraph()
#input = testInput2()
input = readInput()
buildingRules = True
ruleRegex = None
countMatches = 0
rule42 = None
rule31 = None
ruleRe = None

for line in input:
    if buildingRules:
        buildingRules = rulegraph.ParseRule(line)
        if not buildingRules:
            # replace value for rule 8

            expr42 = rulegraph.EvaluateRules(42)
            #rulegraph.replaceEvaluateRule(8, r'('+expr42+')+')
            assert 31 not in rulegraph.evaluatedRules, '31 is already evaluated in rules'
            expr31 = rulegraph.EvaluateRules(31)
            print(f'expr42 = {expr42}\nexpr31 = {expr31}')
            #rulegraph.replaceEvaluateRule(11, r'('+expr42+expr31+|
            #ruleRegex = r'^' + rulegraph.EvaluateRules(0) + r'$'
            ruleRegex = r'^(?P<num42>('+expr42+'(?:'+expr42+')+))(?P<num31>('+expr31+')+?)$'
            ruleRe = re.compile(ruleRegex)
            rule42 = re.compile(expr42)
            rule31 = re.compile(expr31)
            #print(rulegraph.rules)
            #print(rulegraph.evaluatedRules)
            print(f'ruleRe = {ruleRegex}')
            print(f'rule42 = {expr42}')
            print(f'rule31 = {expr31}')
    else:
        #assert ruleRegex is not None, ruleRegex
        assert rule42 is not None
        assert rule31 is not None
        assert ruleRe is not None, ruleRegex
        match = ruleRe.match(line)
        if match is not None:
            print(f"regex match = {match[0]}, num42 = {match['num42']}, num31 = {match['num31']}")
            num42s = rule42.findall( match['num42'] )
            num31s = rule31.findall( match['num31'] )
            if len(num42s) > len(num31s):
                countMatches += 1
        #print('Test:',line, match is not None)
        
print(countMatches)