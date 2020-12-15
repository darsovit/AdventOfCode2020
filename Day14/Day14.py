#!python
import re

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))

def testInput():
    return [
        "mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X",
        "mem[8] = 11",
        "mem[7] = 101",
        "mem[8] = 0"
    ]

class Computer:
    def __init__(self):
        self.mem = {}
        self.mask = None
        maskRE = re.compile(r'^mask = (?P<bitmask>[01X]{36})$')
        memRE  = re.compile(r'^mem\[(?P<memaddr>\d+)\] = (?P<value>\d+)$')
        self.cmds = [ (maskRE, self.__setBitmask), (memRE, self.__setMemory) ]
        
    def runLine(self, line):
        for cmd in self.cmds:
            match = cmd[0].match(line)
            if match is not None:
                cmd[1]( match )
                return
        assert False, 'Failed to find matching cmd with line: {}'.format( line )
    
    def __setBitmask( self, match ):
        maskValue = 0
        maskMask  = 0
        for char in match['bitmask']:
            maskMask <<= 1
            maskValue <<= 1
            if char == 'X':
                maskMask += 1
            elif char == '1':
                maskValue += 1
        self.mask = (maskMask, maskValue)
    
    def __setMemory( self, match ):
        loc = int(match['memaddr'])
        value = int(match['value'])
        self.mem[loc] = ( value & self.mask[0] ) | self.mask[1]
    
    def getMemorySum( self ):
        sum = 0
        print(self.mem)
        for loc in self.mem:
            sum += self.mem[loc]
        return sum
        
comp = Computer()
for line in readInput():
    comp.runLine( line )
print(comp.getMemorySum())