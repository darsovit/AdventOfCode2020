#! python

def testInput():
    return [0,3,6]

def readInput():
    return [14,1,17,0,3,20]

class Memory:
    def __init__(self,initialize):
        self.numbers = initialize.copy()

    def GetNextPosAndNumber(self):
        if self.numbers[-1] not in self.numbers[:-1]:
            self.numbers += [ 0 ]
            return (len(self.numbers), self.numbers[-1])
        else:
            for i in range(len(self.numbers)-1, 0, -1):
                if self.numbers[i-1] == self.numbers[-1]:
                    new_number = len(self.numbers) - i
                    self.numbers += [ new_number ]
                    return (len(self.numbers), self.numbers[-1])
    
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
while nextPosAndNumber[0] != 2020:
    nextPosAndNumber = mem.GetNextPosAndNumber()

print(nextPosAndNumber)


mem = Memory(readInput())
print( mem.GetNextPosAndNumber() )
nextPosAndNumber = mem.GetNextPosAndNumber()
while nextPosAndNumber[0] != 2020:
    nextPosAndNumber = mem.GetNextPosAndNumber()

print( nextPosAndNumber )
