#! python


def readInput():
    with open('input.txt') as f:
        return list(map(int, f.readlines()))

def findSumTo2020( input ):
    values = set()
    for value in input:
        other = 2020 - value
        if other in values:
            return (other, value)
        else:
            values.add(value)

input = readInput()
(x,y) = findSumTo2020( input )
print( x * y )