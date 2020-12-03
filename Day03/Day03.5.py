#!python

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))
        
def countTreeEncountersToBottom(start,deltaX,deltaY,field):
    pos = start
    treeCount = 0
    maxX = len(field[0])
    maxY = len(field)
    pos = ( (pos[0] + deltaX)%maxX, pos[1]+deltaY )
    while ( pos[1] ) < maxY:
        if field[pos[1]][pos[0]] == '#':
            treeCount += 1
        pos = ( (pos[0] + deltaX)%maxX, pos[1]+deltaY )
    return treeCount

lines = readInput()
print(
   countTreeEncountersToBottom((0,0),1,1,lines) *
   countTreeEncountersToBottom((0,0),3,1,lines) *
   countTreeEncountersToBottom((0,0),5,1,lines) *
   countTreeEncountersToBottom((0,0),7,1,lines) *
   countTreeEncountersToBottom((0,0),1,2,lines) )
   
        