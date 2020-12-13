#! python

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))


def decodeInput():
    lines = readInput()
    estimatedEarliest = int(lines[0])
    busIds_str = lines[1].split(',')
    busIds = []
    
    for count, busId_str in enumerate( busIds_str ):
        if busId_str != 'x':
            busIds += [ (int(busId_str),count) ]
    return ( estimatedEarliest, busIds )

def testInput():
    return (939,[(7,0),(13,1),(59,4),(31,6),(19,7)])

def testTimes( testTime, busIdsAndPos ):
    for busIdAndPos in busIdsAndPos:
        if 0 != ( (testTime + busIdAndPos[1]) % busIdAndPos[0]):
            print('testTime {} failed with {}'.format(testTime, busIdAndPos))
            return False
    return True

def findNextFirst( Start, Adder, busIdAndPos ):
    done = testTimes( Start, [busIdAndPos] )
    while not done:
        Start += Adder
        done = testTimes( Start, [busIdAndPos] )
    return Start

def findNextAdder( Start, Adder, busIdAndPos ):
    multiplier = 1
    done = testTimes( Start + (multiplier * Adder), [busIdAndPos] )
    while not done:
        multiplier += 1
        done = testTimes( Start + (multiplier * Adder), [busIdAndPos] )
    return multiplier * Adder

def findConsecutiveTime( busIdsAndPos ):
    busIdsAndPos.sort(reverse=True, key=lambda x: x[0])
    foundRightTime = False
    Adder = busIdsAndPos[0][0]
    Start = busIdsAndPos[0][0]-busIdsAndPos[0][1]
    foundRightTime = testTimes(Start, busIdsAndPos[1:])
    if foundRightTime:
        return (Start)
    for busIdAndPos in busIdsAndPos:
        Start = findNextFirst( Start, Adder, busIdAndPos )
        if testTimes( Start, busIdsAndPos ):
            return (Start)
        Adder = findNextAdder( Start, Adder, busIdAndPos )
        if testTimes( Start, busIdsAndPos ):
            return (Start)
    return (Start)

input = decodeInput()
print( findConsecutiveTime( input[1] ) )
