#!python
import re

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))

def testInput():
    return [
        'mask = 000000000000000000000000000000X1001X',
        'mem[42] = 100',
        'mask = 00000000000000000000000000000000X0XX',
        'mem[26] = 1'
    ]

logp = print
def logp(*kw):
    pass
    
class Computer:
    def __init__(self):
        self.mem = {}
        self.addrValueMask   = 0
        self.addrDynamicMask = (0, '000000000000000000000000000000000000', 0xfffffffff)
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
        maskMask  = ''
        numBitsInMask = 0
        addrDynamicMaskValue = 0
        #print('bitmask:',match['bitmask'])
        for char in match['bitmask']:
            maskValue <<= 1
            addrDynamicMaskValue <<= 1
            
            if char == 'X':
                maskMask += 'X'
                numBitsInMask += 1
            else:
                addrDynamicMaskValue += 1
                maskMask += '0'
                if char == '1':
                    maskValue += 1
        self.addrValueMask = maskValue
        if numBitsInMask > 0:
            #print('numBitsInMask:',numBitsInMask,'maskMask:',maskMask)
            self.addrMask  = ( 1<<numBitsInMask, maskMask, addrDynamicMaskValue )
        else:
            self.addrMask = ( 0, maskMask, addrDynamicMaskValue )
    
    def __getAddrMasks( self ):
        logp('getAddrMasks:', self.addrMask)
        for i in range(self.addrMask[0]):
            addrMaskValue = 0
            addrMaskMask  = 0
            replacements = i
            for j in self.addrMask[1]:
                addrMaskValue <<= 1
                if j == 'X':
                    addrMaskValue += replacements & 1
                    replacements >>= 1
            yield addrMaskValue


    def __getAddresses( self, loc ):
        for maskValue in self.__getAddrMasks():
            addr = (loc & self.addrMask[2]) | maskValue | self.addrValueMask
            logp('loc:', format(loc, 'b'), 'maskValue:', format(maskValue, 'b'), 'addr:', format(addr, 'b'))
            yield addr
            
    def __setMemory( self, match ):
        loc = int(match['memaddr'])
        value = int(match['value'])
        for addr in self.__getAddresses( loc ):
            self.mem[addr] = value
            logp(addr, self.mem[addr])
    
    def getMemorySum( self ):
        sum = 0
        logp(self.mem)
        for loc in self.mem:
            sum += self.mem[loc]
        return sum
        
comp = Computer()
for line in readInput():
    comp.runLine( line )
print(comp.getMemorySum())