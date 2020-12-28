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

    def __repr__(self):
        return '{{id: {}, content: {}, edges: {}}}'.format(self.id, self.content, self.edges)

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
    def __flipBits(edge):
        flippedEdge = 0
        for i in range(10):
            flippedEdge <<= 1
            if edge & (1<<i):
                flippedEdge += 1
        return flippedEdge
        
    def __init__(self, tiles):
        self.length = int( math.sqrt( len(tiles) ) )
        self.state = {}
        self.state['map'] = {}
        self.state['e2t'] = {}
        self.state['tilemap'] = {}
        for tile in tiles:
            self.state['tilemap'][tile.Id()] = tile
            edgeValues = tile.getEdgeValues()
            for edge in edgeValues:
                edgeValue = edgeValues[edge]
                if edgeValue not in self.state['map']:
                    other_edge = Arranger.__flipBits(edgeValue)
                    flippable = (min(edgeValue,other_edge),max(edgeValue,other_edge))
                    self.state['map'][edgeValue] = flippable
                    self.state['map'][other_edge] = flippable
                    self.state['e2t'][flippable] = set()
                    self.state['e2t'][flippable].add((tile.Id(), edge))
                else:
                    self.state['e2t'][self.state['map'][edgeValue]].add((tile.Id(),edge))

    def __findTilesOnEdge(self):
        self.state['imageedges'] = set()
        self.state['tilesOnEdge'] = {}
        for edge in self.state['e2t']:
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

        
        
        
        pass
    def Execute(self):
        self.__findTilesOnEdge()
        cornerList = list( self.__findCorners() )
        if len(cornerList) == 4:
            value = 1
            for corner in cornerList:
                value *= corner[0]
        print(value)

    def __repr__(self):
        return '{{length: {}, state: {}}}'.format(self.length, self.state)

tiles = readTiles(readInput())
arranger = Arranger(tiles)
arranger.Execute()