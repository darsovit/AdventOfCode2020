#!python

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))

def buildGroupAnswer( input ):
    groupAnswer = set()
    for line in input:
        if len(line) == 0:
            yield groupAnswer
            groupAnswer = set()
        for letter in line:
            groupAnswer.add( letter )
    yield groupAnswer

count = 0    
for groupAnswer in buildGroupAnswer( readInput() ):
    count += len( groupAnswer )

print( count )