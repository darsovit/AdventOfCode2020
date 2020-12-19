#! python

def testInput():
    return [0,3,6]

def readInput():
    return [14,1,17,0,3,20]

class Memory:
    def __init__(self,initialize):
        self.numbers = {}
        self.count   = len(initialize)
        self.last    = initialize[-1]
        for (count,numbers) in enumerate(initialize[:-1]):
            self.numbers[numbers] = count+1
        

    def GetNextPosAndNumber(self):
        if self.last not in self.numbers:
            self.numbers[self.last] = self.count
            self.last = 0
        else:
            newlast = self.count - self.numbers[self.last]
            self.numbers[self.last] = self.count
            self.last = newlast
        self.count += 1
        return (self.count,self.last)
        
    def __repr__(self):
        return '{}'.format(self.numbers)

mem = Memory(testInput())
print( mem.GetNextPosAndNumber() )
print( mem.GetNextPosAndNumber() )
print( mem.GetNextPosAndNumber() )
print( mem.GetNextPosAndNumber() )
print( mem.GetNextPosAndNumber() )
print( mem.GetNextPosAndNumber() )
print( mem.GetNextPosAndNumber() )

nextPosAndNumber = mem.GetNextPosAndNumber()
while nextPosAndNumber[0] != 30000000:
    nextPosAndNumber = mem.GetNextPosAndNumber()

print(nextPosAndNumber)


mem = Memory(readInput())
print( mem.GetNextPosAndNumber() )
nextPosAndNumber = mem.GetNextPosAndNumber()
while nextPosAndNumber[0] != 30000000:
    nextPosAndNumber = mem.GetNextPosAndNumber()

print( nextPosAndNumber )
