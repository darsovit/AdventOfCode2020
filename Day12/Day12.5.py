#!python

import re

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))

def testInput():
    return [
        'F10',
        'N3',
        'F7',
        'R90',
        'F11']

class Navigator:
    def __init__(self):
        self.pos    = (0,0)
        self.waypoint = (10,1)
        self.reInstr = re.compile(r'^(?P<ins>[NSEWLRF])(?P<count>\d+)$')

    def followDirection( self, instr ):
        match = self.reInstr.match( instr )
        count = int(match['count'])
        assert match, 'Unknown instruction: {}'.format(instr)
        if match['ins'] == 'L':
            self.turnLeft(count)
        elif match['ins'] == 'R':
            self.turnRight(count)
        elif match['ins'] == 'F':
            self.moveForward(count)
        elif match['ins'] == 'N':
            self.moveNorth(count)
        elif match['ins'] == 'S':
            self.moveSouth(count)
        elif match['ins'] == 'E':
            self.moveEast(count)
        elif match['ins'] == 'W':
            self.moveWest(count)
        else:
            assert False, 'Unknown instruction: {}'.format(instr)

    def turnLeft(self, count):
        # (2,1) -> (-1,2) -> (-2,-1) -> (1,-2)
        
        if count == 90:            
            self.waypoint = ( self.waypoint[1] * -1, self.waypoint[0] )
        elif count == 180:
            self.turnAround()
        elif count == 270:
            self.turnRight(90)
        else:
            assert False, 'Unknown count {} for turning left'.format(count)

    def turnRight(self,count):
        # (2,1) -> (1,-2) -> (-2,-1) -> (-1,2)
        if count == 90:
            self.waypoint = ( self.waypoint[1], self.waypoint[0] * -1 )
        elif count == 180:
            self.turnAround()
        elif count == 270:
            self.turnLeft(90)
        else:
            assert False, 'Unknown count {} for turning right'.format(count)
            
    def moveForward(self, count):
        self.pos = (self.pos[0] + self.waypoint[0] * count, self.pos[1] + self.waypoint[1] * count )
    
    def moveEast(self, count):
        self.waypoint = (self.waypoint[0]+count, self.waypoint[1])
    def moveWest(self, count):
        self.waypoint = (self.waypoint[0]-count, self.waypoint[1])
    def moveNorth(self, count):
        self.waypoint = (self.waypoint[0], self.waypoint[1]+count)
    def moveSouth(self, count):
        self.waypoint = (self.waypoint[0], self.waypoint[1]-count)
    
    def getPosition(self):
        return self.pos
    
    def turnAround(self):
        self.waypoint = ( self.waypoint[0] * -1, self.waypoint[1] * -1 )
        
navigation = Navigator()
for line in readInput():
    navigation.followDirection(line)
newpos = navigation.getPosition()
print(newpos)
print( newpos[0] + newpos[1] )