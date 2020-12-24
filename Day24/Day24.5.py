#!python

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))

class LobbyFloorHexTiles:
    def __init__(self):
        self.__blacktiles = set()
        self.__numDays    = 0
        self.__extents    = [0,0,0,0] # minX, minY, maxX, maxY

    def __AddBlackTile(self, pos):
        if pos[0] < self.__extents[0]:
            self.__extents[0] = pos[0]
        elif pos[0] > self.__extents[2]:
            self.__extents[2] = pos[0]
        if pos[1] < self.__extents[1]:
            self.__extents[1] = pos[1]
        elif pos[1] > self.__extents[3]:
            self.__extents[3] = pos[1]
        self.__blacktiles.add(pos)

    def HandleInstructionList(self, instructions):
        if instructions == '':
            return
        pos = (0,0)
        savedY = None
        for instruction in instructions:
            if instruction in ('n','s'):
                assert savedY is None
                savedY = instruction
            else:
                if instruction == 'e':
                    if savedY:
                        pos = (pos[0]+1,pos[1] + (1 if savedY == 'n' else -1))
                        savedY = None
                    else:
                        pos = (pos[0]+2,pos[1])
                else:
                    assert instruction == 'w'
                    if savedY:
                        pos = (pos[0]-1,pos[1] + (1 if savedY == 'n' else -1))
                        savedY = None
                    else:
                        pos = (pos[0]-2,pos[1])
        assert savedY is None
        if pos in self.__blacktiles:
            self.__blacktiles.remove(pos)
        else:
            self.__AddBlackTile(pos)

    def __getNeighbors(pos):
        neighborPositions = [(2,0),(-2,0),(1,1),(-1,1),(1,-1),(-1,-1)]
        for neighborPos in neighborPositions:
            yield (pos[0]+neighborPos[0],pos[1]+neighborPos[1])

    def HandleDayFlip(self):
        blacktiles = self.__blacktiles
        extents    = self.__extents
        self.__resetTiles()
        for y in range(extents[1]-1,extents[3]+2):
            minX = extents[0] + ( -2 if y % 2 == extents[0] % 2 else -3 )
            maxX = extents[2] + ( 2 if y % 2 == extents[2] % 2 else 3 )
            for x in range(minX,maxX + 2, 2):
                pos = (x,y)
                countBlackTileNeighbors = 0
                for neighbor in LobbyFloorHexTiles.__getNeighbors(pos):
                    if neighbor in blacktiles:
                        countBlackTileNeighbors += 1
                if pos in blacktiles and countBlackTileNeighbors in [1,2]:
                    self.__AddBlackTile(pos)
                if pos not in blacktiles and countBlackTileNeighbors == 2:
                    self.__AddBlackTile(pos)
                #print('pos {} which is {} has {} black tile neighbors'.format(pos, 'black' if pos in blacktiles else 'white', countBlackTileNeighbors))
        self.__numDays += 1                    

    def __resetTiles(self):
        self.__blacktiles = set()
        self.__extents = [0,0,0,0]

    def __repr__(self):
        return '{{__numDays: {}, __extents: {}, __blacktiles: {}}}'.format(self.__numDays, self.__extents, self.__blacktiles)

    def countOfBlackTiles(self):
        return len(self.__blacktiles)

    def getDayCount(self):
        return self.__numDays

def testInput():
    return '''sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
'''.split('\n')

def runInstructions(input):
    floor = LobbyFloorHexTiles()
    for line in input:
        #print(line, floor)
        floor.HandleInstructionList(line)
    #print(floor)
    return floor
    
testFloor = runInstructions(testInput())
assert testFloor.countOfBlackTiles() == 10, testFloor

testResults = {1: 15, 2: 12, 3: 25, 4: 14, 5: 23, 6: 28, 7: 41, 8: 37, 9: 49, 10: 37,
               20: 132, 30: 259, 40: 406, 50: 566, 60: 788, 70: 1106, 80:1373, 90:1844, 100: 2208}

for i in range(max(list(testResults.keys()))):
    testFloor.HandleDayFlip()
    day = testFloor.getDayCount()
    if day in testResults:
        expectedBlackTiles = testResults[day]
        countBlackTiles    = testFloor.countOfBlackTiles()
        assert expectedBlackTiles == countBlackTiles, '{} != {} on day {}'.format(expectedBlackTiles, countBlackTiles, day)


realFloor = runInstructions(readInput())
for i in range(100):
    realFloor.HandleDayFlip()
print(realFloor.countOfBlackTiles())