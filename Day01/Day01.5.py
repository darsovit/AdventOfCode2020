#! python


def readInput():
    with open('input.txt') as f:
        return list(map(int, f.readlines()))

def findSumToTotal( total, input ):
    values = set()
    for value in input:
        other = total - value
        if other in values:
            return (other, value)
        else:
            values.add(value)
    return None

def findTripleSumTo2020( input ):
    for i in range(len(input)):
        someVal = input[i]
        otherTotal = 2020 - someVal
        otherValues = findSumToTotal( otherTotal, input[:i] + input[i+1:] )
        if otherValues is not None:
            return ( someVal, otherValues[0], otherValues[1] )

input = readInput()
(x,y,z) = findTripleSumTo2020( input )
print( x * y * z )