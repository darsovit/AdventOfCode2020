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
        self.facing = 'E'
        self.pos    = (0,0)
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
        if count == 90:
            if self.facing == 'E':
                self.facing = 'N'
            elif self.facing == 'N':
                self.facing = 'W'
            elif self.facing == 'W':
                self.facing = 'S'
            else:
                assert self.facing == 'S', 'Unknown current facing: {} for turning left {}'.format(self.facing, count)
                self.facing = 'E'
        elif count == 180:
            self.turnAround()
        elif count == 270:
            self.turnRight(90)
        else:
            assert False, 'Unknown count {} for turning left'.format(count)

    def turnRight(self,count):
        if count == 90:
            if self.facing == 'E':
                self.facing = 'S'
            elif self.facing == 'S':
                self.facing = 'W'
            elif self.facing == 'W':
                self.facing = 'N'
            else:
                assert self.facing == 'N', 'Unknown current facing: {} for turning right {}'.format(self.facing, count)
                self.facing = 'E'
        elif count == 180:
            self.turnAround()
        elif count == 270:
            self.turnLeft(90)
        else:
            assert False, 'Unknown count {} for turning right'.format(count)
            
    def moveForward(self, count):
        if self.facing == 'N':
            self.moveNorth(count)
        elif self.facing == 'E':
            self.moveEast(count)
        elif self.facing == 'W':
            self.moveWest(count)
        else:
            assert self.facing == 'S', 'Current direction {} is unknown to move forward {}'.format(self.facing, count)
            self.moveSouth(count)
    
    def moveEast(self, count):
        self.pos = (self.pos[0]+count, self.pos[1])
    def moveWest(self, count):
        self.pos = (self.pos[0]-count, self.pos[1])
    def moveNorth(self, count):
        self.pos = (self.pos[0], self.pos[1]+count)
    def moveSouth(self, count):
        self.pos = (self.pos[0], self.pos[1]-count)
    
    def getPosition(self):
        return self.pos
    
    def turnAround(self):
        self.turnLeft(90)
        self.turnLeft(90)
        
navigation = Navigator()
for line in readInput():
    navigation.followDirection(line)
print( navigation.getPosition() )