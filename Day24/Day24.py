#!python

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))

class LobbyFloorHexTiles:
    def __init__(self):
        self.__blacktiles = set()
    
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
            self.__blacktiles.add(pos)

    def __repr__(self):
        return '{{__blacktiles: {}}}'.format(self.__blacktiles)

    def countOfBlackTiles(self):
        return len(self.__blacktiles)

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
    return floor.countOfBlackTiles()
    
numInTest = runInstructions(testInput())
assert numInTest == 10, numInTest

print(runInstructions(readInput()))