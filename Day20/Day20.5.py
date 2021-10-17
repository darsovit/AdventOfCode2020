#! python

import math

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))

def testInput():
    return list('''Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
'''.split('\n'))


class Tile:
    def __init__(self, id, content):
        self.id = id
        self.content = content
        self.edges   = self.__calculateEdges()
        self.edgeIds = self.__updateIds()

    def __flipBits(edge):
        flippedEdge = 0
        for i in range(10):
            flippedEdge <<= 1
            if edge & (1<<i):
                flippedEdge += 1
        return flippedEdge

    def __updateIds(self):
        edgeIds = {}
        for name in ('top', 'bottom', 'left', 'right'):
            edgeIds[name] = min(self.edges[name],Tile.__flipBits(self.edges[name]))
        return edgeIds

    def __calculateEdges(self):
        edgeValues = { 'top':    0,
                       'right':  0,
                       'bottom': 0,
                       'left':   0 }
        faredge    = len(self.content)-1
        #top = ''
        #right = ''
        #bottom = ''
        #left = ''
        
        for i in range(len(self.content)):
        #    top    = top + self.content[0][i]
        #    right  = right + self.content[i][faredge]
        #    bottom = bottom + self.content[faredge][-1*(i+1)]
        #    left   = left   + self.content[-1*(i+1)][0]
            edgeValues['top']    = (edgeValues['top']    << 1) + ( 1 if self.content[0][i] == '#' else 0 )
            edgeValues['right']  = (edgeValues['right']  << 1) + ( 1 if self.content[i][faredge] == '#' else 0 )
            edgeValues['bottom'] = (edgeValues['bottom'] << 1) + ( 1 if self.content[faredge][-1 * (i+1)] == '#' else 0)
            edgeValues['left']   = (edgeValues['left']   << 1) + ( 1 if self.content[-1 * (i+1)][0] == '#' else 0)
        #print('top   : {}, edgeValues[top]   : {}', top,    edgeValues['top'])
        #print('right : {}, edgeValues[right] : {}', right,  edgeValues['right'])
        #print('bottom: {}, edgeValues[bottom]: {}', bottom, edgeValues['bottom'])
        #print('left  : {}, edgeValues[left]  : {}', left,   edgeValues['left'])
        #print('content:')
        #for line in self.content:
        #    print(line)        
        return edgeValues


    def Id(self):
        return self.id

    def getEdgeValues(self):        
        return self.edges
        
    def getEdgeIds(self):
        return self.edgeIds


    def __rotateCCW(self):
        #print(f'pre-CCW: {self}')
        contentToStrip = self.content
        newContent = []
        for i in range(len(contentToStrip[0])-1,-1,-1):
            line = ""
            for j in range(len(contentToStrip)):
                line += contentToStrip[j][i]
            newContent += [ line ]
        newTile = Tile(self.id, newContent)
        #print(f'post-CCW: {newTile}')
        return newTile

    def __rotateCW(self):
        #print(f'pre-CW: {self}')
        contentToStrip = self.content
        newContent = []
        for i in range(len(contentToStrip[0])):
            line = ""
            for j in range(len(contentToStrip)-1,-1,-1):
                line += contentToStrip[j][i]
            newContent += [ line ]
        newTile = Tile(self.id, newContent)
        #print(f'post-CW: {newTile}')
        return newTile

    def __flipLeftToRight(self):
        #print(f'preLtoR: {self}')
        newContent = []
        for line in self.content:
            newContent += [ line[::-1] ]
        newTile = Tile(self.id, newContent)
        #print(f'postLtoR: {newTile}')
        return newTile

    def __flipTopToBottom(self):
        #print(f'preTtoB: {self}')
        newContent = []
        for i in range(len(self.content)-1, -1, -1):
            newContent += [ self.content[i] ]
        newTile = Tile(self.id, newContent)
        #print(f'postToB: {newTile}')
        return newTile


    def orient(self, left, top):
        #print(f'orient: left={left} top={top}')
        if left == self.edgeIds['top']:
            return self.__rotateCCW().orient(left, top)
        if left == self.edgeIds['bottom']:
            return self.__rotateCW().orient(left, top)
        if left == self.edgeIds['right']:
            return self.__flipLeftToRight().orient(left, top)
        
        assert left == self.edgeIds['left']
        if top == self.edgeIds['bottom']:
            return self.__flipTopToBottom()
        assert top == self.edgeIds['top']
        return self
        
    def __getContent(self):
        out = "\n"
        for line in self.content:
            out += line + "\n"
        return out

    def __repr__(self):
        return '{{id: {}, edgeIds: {}, content: {}}}'.format(self.id, self.edgeIds, self.__getContent())

    def Content(self):
        newContent = []
        for line in self.content[1:-1]:
            newContent += [ line[1:-1] ]
        return newContent

def readTiles(input):
    content = []
    id      = None
    tiles   = []
    foundLength = None
    for line in input:
        if line == '':
            assert id is not None
            if foundLength is None:
                assert len(content) > 0
                foundLength = len(content)
            assert len(content) > 0 and len(content) == foundLength and len(content[0]) == foundLength
            tiles += [ Tile(id, content) ]
            id = None
            content = []
        elif line.startswith('Tile ') and line.endswith(':'):
            id = int(line[5:-1])
        else:
            content += [ line ]
    if id is not None and len(content) > 0:
        tiles += [Tile(id, content)]
    return tiles


class Arranger:
    def __init__(self, tiles):
        self.state = {}
        self.state['e2t'] = {}
        self.tilemap = {}
        self.availableTiles = set()
        for tile in tiles:
            self.tilemap[tile.Id()] = tile
            self.availableTiles.add(tile.Id())
            edgeValues = tile.getEdgeIds()
            for edge in edgeValues:
                edgeId = edgeValues[edge]
                if edgeId not in self.state['e2t']:
                    self.state['e2t'][edgeId] = []
                self.state['e2t'][edgeId] += [ (tile.Id(), edge) ]
        self.state['positions'] = []
        
    def __findTilesOnEdge(self):
        self.state['imageedges'] = set()
        self.state['tilesOnEdge'] = {}
        for edge in self.state['e2t']:
            assert len(self.state['e2t'][edge]) < 3, f'Found more than two tiles for edge id: {edge}'
            if len(self.state['e2t'][edge]) == 1:
                (tileId,side) = list(self.state['e2t'][edge])[0]
                if tileId not in self.state['tilesOnEdge']:
                    self.state['tilesOnEdge'][tileId] = set()
                self.state['tilesOnEdge'][tileId].add(side)
                self.state['imageedges'].add(edge)
        
    def __findCorners(self):
        for tile in self.state['tilesOnEdge']:
            if len(self.state['tilesOnEdge'][tile]) > 1:
                assert len(self.state['tilesOnEdge'][tile]) == 2, 'tile: {}, solo edges: {}\nstate: {}'.format(tile, self.state['tilesOnEdge'][tile], self.state )
                yield (tile, self.state['tilesOnEdge'][tile])

    def __getNextTileByEdgeId(self, nextId):
        matchingTiles = self.state['e2t'][nextId]
        for matchingTile in matchingTiles:
            if matchingTile[0] in self.availableTiles:
                return matchingTile
        #print(f'nextId: {nextId}, matchingTiles: {matchingTiles}')
        return None

    def __buildTopRow(self):
        pos = (0,0)
        def getRightTile(pos):
            nextTileLeftId = self.__image[pos].getEdgeIds()['right']
            return self.__getNextTileByEdgeId(nextTileLeftId)

        def determineNextLeftTopEdgeIds( tileInfo ):
            matchedEdge = tileInfo[1]
            tile = self.tilemap[tileInfo[0]]
            edgeIdsForTile = tile.getEdgeIds()
            
            if matchedEdge in {'bottom','top'}:
                if edgeIdsForTile['left'] in self.state['e2t'] and len(self.state['e2t'][edgeIdsForTile['left']]) == 1:
                    return (edgeIdsForTile[matchedEdge],edgeIdsForTile['left'])
                assert edgeIdsForTile['right'] in self.state['e2t'] and len(self.state['e2t'][edgeIdsForTile['right']]) == 1
                return (edgeIdsForTile[matchedEdge],edgeIdsForTile['right'])
            assert matchedEdge in {'left', 'right'}
            if edgeIdsForTile['top'] in self.state['e2t'] and len(self.state['e2t'][edgeIdsForTile['top']]) == 1:
                return (edgeIdsForTile[matchedEdge],edgeIdsForTile['top'])
            assert edgeIdsForTile['bottom'] in self.state['e2t'] and len(self.state['e2t'][edgeIdsForTile['bottom']]) == 1
            return (edgeIdsForTile[matchedEdge],edgeIdsForTile['bottom'])

        nextTile       = getRightTile(pos)
        while nextTile:
            (leftId, topId) = determineNextLeftTopEdgeIds( nextTile )
            nextPos = (0,pos[1]+1)
            self.__image[nextPos] = self.tilemap[nextTile[0]].orient(leftId, topId)
            assert len(self.state['e2t'][self.__image[nextPos].getEdgeIds()['bottom']]) > 1
            self.availableTiles.remove(self.__image[nextPos].Id())
            pos = nextPos
            nextTile = getRightTile(pos)
        #while nextTileLeftId:
        #print(f'{self.__image}')
        self.width = pos[1] + 1
    
    def __buildLeftEdge(self):
        pos = (0,0)
        def getBottomTile(pos):
            nextTileTopId = self.__image[pos].getEdgeIds()['bottom']
            return self.__getNextTileByEdgeId(nextTileTopId)
            
        def determineNextLeftTopEdgeIds( tileInfo ):
            matchedEdge = tileInfo[1]
            tile = self.tilemap[tileInfo[0]]
            edgeIdsForTile = tile.getEdgeIds()
            if matchedEdge in {'bottom', 'top'}:
                if edgeIdsForTile['left'] in self.state['e2t'] and len(self.state['e2t'][edgeIdsForTile['left']]) == 1:
                    return (edgeIdsForTile['left'],edgeIdsForTile[matchedEdge])
                assert edgeIdsForTile['right'] in self.state['e2t'] and len(self.state['e2t'][edgeIdsForTile['right']]) == 1
                return (edgeIdsForTile['right'],edgeIdsForTile[matchedEdge])
            assert matchedEdge in {'left','right'}
            if edgeIdsForTile['top'] in self.state['e2t'] and len(self.state['e2t'][edgeIdsForTile['top']]) == 1:
                return (edgeIdsForTile['top'], edgeIdsForTile[matchedEdge])
            assert edgeIdsForTile['bottom'] in self.state['e2t'] and len(self.state['e2t'][edgeIdsForTile['bottom']]) == 1
            return (edgeIdsForTile['bottom'], edgeIdsForTile[matchedEdge])
        
        nextTile = getBottomTile(pos)
        while nextTile:
            (leftId,topId) = determineNextLeftTopEdgeIds( nextTile )
            nextPos = (pos[0]+1,0)
            self.__image[nextPos] = self.tilemap[nextTile[0]].orient(leftId,topId)
            self.availableTiles.remove(self.__image[nextPos].Id())
            pos = nextPos
            nextTile = getBottomTile(pos)
        self.height = pos[0]+1
        
    
    def __fillInImage(self):
        #print(f'height = {self.height}, width = {self.width}')
        def getTileForPos( pos ):
            leftId = self.__image[(pos[0],pos[1]-1)].getEdgeIds()['right']
            topId  = self.__image[(pos[0]-1,pos[1])].getEdgeIds()['bottom']
            fromLeftTile = self.__getNextTileByEdgeId( leftId )
            fromTopTile  = self.__getNextTileByEdgeId( topId )
            try:
                assert fromLeftTile[0] == fromTopTile[0]
            except:
                print(f'pos={pos}, left: {leftId} = {fromLeftTile}, top: {topId} = {fromTopTile}')
                raise
            return self.tilemap[fromLeftTile[0]].orient(leftId, topId)
            
        for i in range(1,self.height):
            for j in range(1,self.width):
                pos = (i,j)
                try:
                    self.__image[pos] = getTileForPos(pos)
                except:
                    print(f'{self.__image}')
                    raise
                self.availableTiles.remove(self.__image[pos].Id())
        
        #print( self.__image )
        
    def __buildStartTile(self):
        startTileInfo = self.__corners[0]
        startTile     = self.tilemap[startTileInfo[0]]
        bareEdgeNames = list(startTileInfo[1])
        leftEdgeId    = startTile.getEdgeIds()[bareEdgeNames[0]]
        topEdgeId     = startTile.getEdgeIds()[bareEdgeNames[1]]
        pos = (0,0)
        self.__image = {}
        self.__image[pos] = startTile.orient(topEdgeId,leftEdgeId)
        self.availableTiles.remove(startTile.Id())
        #print(self.__image[pos])

    def __collectImage(self):
        content = []
        contentHeightBase = 0
        for i in range(0,self.height):
            tileHeight = None
            for j in range(0,self.width):
                tileContent = self.__image[(i,j)].Content()
                assert tileHeight is None or len(tileContent) == tileHeight
                tileHeight = len(tileContent)
                if (j == 0):
                    for k in range(len(tileContent)):
                        content += [""]
                for k in range(len(tileContent)):
                    content[k+contentHeightBase] += tileContent[k]
            contentHeightBase += tileHeight
        self.__contentImage = content
        
    def __buildImage(self):
        self.__buildStartTile()
        self.__buildTopRow()
        self.__buildLeftEdge()
        self.__fillInImage()
        self.__collectImage()
        
    def Execute(self):
        sides = {'top','left','bottom','right'}
        self.__findTilesOnEdge()
        self.__corners = list(self.__findCorners())
        self.__buildImage()
        return self.__contentImage

    def __repr__(self):
        return '{{length: {}, state: {}}}'.format(self.length, self.state)

class MonsterFinder:
    def __init__(self, picture):
        self.__picture = picture
        self.__countPixels()
        
    def __MonsterDef(self):
        '''
                          # 
        #    ##    ##    ###
         #  #  #  #  #  # 
        ''' 
        return [(1,0),(2,1),(2,4),(1,5),(1,6),(2,7),(2,10),(1,11),(1,12),(2,13),(2,16),(1,17),(0,18),(1,18),(1,19)]

    def __countPixels(self):
        numPixels = 0
        for i in range(len(picture)):
            for j in range(len(picture[i])):
                numPixels += 1 if picture[i][j] == '#' else 0
        self.__numPixels = numPixels

    def Execute(self):
        monster = self.__MonsterDef()
        numMonsters = 0
        monsterPos = []
        for i in range(len(picture)-2):
            for j in range(len(picture[i])-19):
                found = True
                for pixel in monster:
                    found = self.__picture[i+pixel[0]][j+pixel[1]] == '#'
                    if not found:
                        break
                if found:
                    numMonsters += 1
                    monsterPos += [(i,j)]
        print(numMonsters)
        return (numMonsters, self.__numPixels - (numMonsters*len(monster)))
                    
    
    
#tiles = readTiles(testInput())
tiles = readTiles(readInput())
arranger = Arranger(tiles)
#print(f"{arranger.state['e2t']}")
picture = arranger.Execute()

for line in picture:
    print(f'{line}')
finder = MonsterFinder(picture)
numMonsters = finder.Execute()
print(numMonsters)
