#!python

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))

def testInput():
    return [
        'L.LL.LL.LL',
        'LLLLLLL.LL',
        'L.L.L..L..',
        'LLLL.LL.LL',
        'L.LL.LL.LL',
        'L.LLLLL.LL',
        '..L.L.....',
        'LLLLLLLLLL',
        'L.LLLLLL.L',
        'L.LLLLL.LL' ]

def checkSeatIsOccupied( orig, direction, input ):
    multiplier = 1
    while True:
        pos = (orig[0] + direction[0]*multiplier, orig[1] + direction[1]*multiplier)
        if pos[0] >= len(input) or pos[0] < 0:
            return False
        if pos[1] >= len(input[pos[0]]) or pos[1] < 0:
            return False
        if (input[pos[0]][pos[1]] == '#'):
            return True
        if (input[pos[0]][pos[1]] == 'L'):
            return False
        multiplier += 1

adjacencies = [(-1,-1),(-1,0),(-1,1),
               ( 0,-1),       ( 0,1),
               ( 1,-1),( 1,0),( 1,1) ]

def countAdjacentOccupiedSeats( pos, input ):
    occupiedCount = 0
    for adjacent in adjacencies:
        if checkSeatIsOccupied(pos, adjacent, input):
            occupiedCount += 1
    return occupiedCount

def fillSeatsPerRules( input ):
    newSeats = []
    for i in range(len(input)):
        newSeats += [[]]
        for j in range(len(input[i])):
            if input[i][j] == '.':
                newSeats[i] += ['.']
            else:
                occupiedCount = countAdjacentOccupiedSeats((i,j),input)
                if 0 == occupiedCount:
                    newSeats[i] += ['#']
                elif occupiedCount >= 5:
                    newSeats[i] += ['L']
                else:
                    newSeats[i] += [input[i][j]]
    return newSeats

def findStability(input):
    nextSeats = fillSeatsPerRules( input )
    done = False
    while not done:
        oldSeats = nextSeats.copy()
        nextSeats = fillSeatsPerRules( oldSeats )
        done = ( oldSeats == nextSeats )
    return nextSeats

def countAllOccupiedSeats(input):
    allOccupiedSeats = 0
    for row in input:
        for col in row:
            if '#' == col:
                allOccupiedSeats += 1
    return allOccupiedSeats

print(countAllOccupiedSeats(findStability(testInput())))
