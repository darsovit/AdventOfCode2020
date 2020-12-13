#! python

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))


def decodeInput():
    lines = readInput()
    estimatedEarliest = int(lines[0])
    busIds_str = lines[1].split(',')
    busIds = []
    for busId_str in busIds_str:
        if busId_str != 'x':
            busIds += [ int(busId_str) ]
    return ( estimatedEarliest, busIds )

def testInput():
    return (939,[7,13,59,31,19])

def findEarliestBusId( estimatedEarliest, busIds ):
    earliestBus = None
    for busId in busIds:
        howLongSinceLastBus = estimatedEarliest % busId
        waitTilNext = busId - howLongSinceLastBus
        if earliestBus is None or waitTilNext < earliestBus[0]:
            earliestBus = (waitTilNext, busId)
    return earliestBus
    

input = testInput()
print( 'testInput():', findEarliestBusId( input[0], input[1] ) )

input = decodeInput()
earliestBusDetails = findEarliestBusId( input[0], input[1] )
print( 'decodeInput():', earliestBusDetails, earliestBusDetails[0] * earliestBusDetails[1] )