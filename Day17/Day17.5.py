#! python

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))

def testInput():
    return [ '.#.', '..#', '###' ]
    
class ConwayCubeCalculator:
    def __init__(self, input):
        self.state = set()
        self.limits  = None
        for (y,line) in enumerate(input):
            for (x,item) in enumerate(line):
                if '#' == item:
                    self.__activateCube((x,y,0,0))
        self.life = 0

    def __updateLimits(self, pos):
        if self.limits is None:
            self.limits = [(pos[0],pos[0]),(pos[1],pos[1]),(pos[2],pos[2]),(pos[3],pos[3])]
        else:
            for i in range(4):
                if pos[i] < self.limits[i][0]:
                    self.limits[i] = (pos[i], self.limits[i][1])
                elif pos[i] > self.limits[i][1]:
                    self.limits[i] = (self.limits[i][0], pos[i])
    
    def __activateCube(self, pos):
        self.state.add(pos)
        self.__updateLimits(pos)

    def step(self):
        limits = self.limits.copy()
        state  = self.state
        self.state = set()
        self.limits = None
        for x in range(limits[0][0]-1, limits[0][1]+2):
            for y in range(limits[1][0]-1, limits[1][1]+2):
                for z in range(limits[2][0]-1, limits[2][1]+2):
                    for w in range(limits[3][0]-1, limits[3][1]+2):
                        if self.__determineActiveFromState((x,y,z,w),state):
                            self.__activateCube((x,y,z,w))
        self.life += 1

    def __determineActiveFromState(self, pos, state):
        countActiveNeighbors = 0
        for neighbor in self.__getNeighbors(pos):
            if neighbor in state:
                countActiveNeighbors += 1
        return ( countActiveNeighbors == 3 or ( pos in state and countActiveNeighbors == 2) )

    def __getNeighbors(self, pos):
        for w in [-1,1]:
            for z in [-1,0,1]:
                for x in [-1,0,1]:
                    for y in [-1,0,1]:
                        yield(x+pos[0],y+pos[1],z+pos[2],w+pos[3])

        for z in [-1,1]:
            for x in [-1,0,1]:
                for y in [-1,0,1]:
                    yield (x+pos[0],y+pos[1],z+pos[2],pos[3])

        for x in [-1,1]:
            for y in [-1,0,1]:
                yield (x+pos[0],y+pos[1],pos[2],pos[3])
        
        for y in [-1,1]:
            yield (pos[0],y+pos[1],pos[2],pos[3])


    def __repr__(self):
        ourRepr = 'life = {}\n'.format(self.life)
        for w in range(self.limits[3][0],self.limits[3][1]+1):
            
            for z in range(self.limits[2][0],self.limits[2][1]+1):
                ourRepr += 'z = {}, w = {}\n'.format(z, w)
                for y in range(self.limits[1][0],self.limits[1][1]+1):
                    for x in range(self.limits[0][0], self.limits[0][1]+1):
                        if (x,y,z) in self.state:
                            ourRepr += '#'
                        else:
                            ourRepr += '.'
                    ourRepr += '\n'
        return ourRepr
    
    def howManyActiveCubes(self):
        return len(self.state)
        
calculator = ConwayCubeCalculator(readInput())
for i in range(6):
    calculator.step()

print(calculator.howManyActiveCubes())