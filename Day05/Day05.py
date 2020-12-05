#!python

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))
        
def calcSeatValue( seatCode ):
    value = 0
    for code in seatCode:
        if code in ['B','R']:
            value = (value << 1) + 1
        else:
            value = value << 1
    return value

def testValue( seatCode, expected ):
    assert expected == calcSeatValue( seatCode ), '{} != ({} = calcSeatValue({}))'.format(expected, calcSeatValue(seatCode), seatCode)

testValue('FBFBBFFRLR', 357)
testValue('BFFFBBFRRR', 567)
testValue('FFFBBBFRRR', 119)
testValue('BBFFBBFRLL', 820)

print( max(map(calcSeatValue, readInput())) )