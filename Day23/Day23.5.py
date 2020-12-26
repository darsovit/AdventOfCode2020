#!python

class CrabCup:
    def __init__(self, value):
        self.__next = None
        self.__value = value
    
    def SetNext(self, next):
        assert self.__next is None
        self.__next = next

    def GetNext(self):
        assert self.__next is not None
        return self.__next
    
    def ResetNext(self, next=None):
        assert self.__next is not None
        self.__next = next

    def Value(self):
        return self.__value

class CrabCupsMega:
    def __init__(self, input, numOfCups):
        self.cups = {}
        assert len(input) <= numOfCups, 'Asking for less cups than given input'
        self.cups[input[0]] = CrabCup(input[0])
        lastcup = input[0]
        firstcup = input[0]
        for i in input[1:]:
            self.cups[i] = CrabCup(i)
            self.cups[lastcup].SetNext( self.cups[i] )
            lastcup = i
        for i in range(len(input)+1, numOfCups+1):
            self.cups[i] = CrabCup(i)
            self.cups[lastcup].SetNext( self.cups[i] )
            lastcup = i
        self.cups[lastcup].SetNext(self.cups[firstcup])
        self.max = numOfCups
        self.pos = firstcup
        self.rounds = 0

    def __nextLower(self, value):
        return (((value - 2) + self.max) % self.max) + 1

    def playRound(self):
        (saved_cups_values,savedcups)  = self.__getSavedCups()
        #print(saved_cups)
        findvalue   = self.__nextLower( self.__getValue(self.pos) )
        while findvalue in saved_cups_values:
            findvalue = self.__nextLower( findvalue )
            #print('findvalue:',findvalue,findvalue in saved_cups)
        #print('findvalue:',findvalue)
        #print('newpos:',newpos)
        self.rounds += 1
        self.__shiftCupsAndAdjustPos( findvalue, savedcups )

    def __getSavedCups( self ):
        countCups = 0
        firstsavedcup = self.cups[self.pos].GetNext()
        thirdsavedcup = firstsavedcup.GetNext().GetNext()
        self.cups[self.pos].ResetNext(thirdsavedcup.GetNext())
        thirdsavedcup.ResetNext()
        return ([firstsavedcup.Value(),firstsavedcup.GetNext().Value(),thirdsavedcup.Value()],firstsavedcup)

    def __getValue( self, pos ):
        return self.cups[pos].Value()
    
    def __shiftCupsAndAdjustPos( self, newpos, saved_cups ):
        saved_cups.GetNext().GetNext().SetNext( self.cups[newpos].GetNext() )
        self.cups[newpos].ResetNext( saved_cups )
        self.pos = self.cups[self.pos].GetNext().Value()
        assert self.pos == self.cups[self.pos].Value()

    def __repr__(self):
        gamestate = '({})'.format(self.pos)
        assert self.pos == self.cups[self.pos].Value()
        nextcup = self.cups[self.pos].GetNext()
        while nextcup.Value() != self.pos:
            gamestate = gamestate + ',{}'.format(nextcup.Value())
            nextcup = nextcup.GetNext()
        return '{{rounds: {}, pos: {}, state: {}}}'.format(self.rounds, self.pos, gamestate)

    def PresentResult(self):
        nextvalue = self.cups[1].GetNext().Value()
        furthervalue = self.cups[1].GetNext().GetNext().Value()
        print( '1,{},{},...'.format(nextvalue,furthervalue) )
        print( 'multiplied:', nextvalue * furthervalue )

def test():
    game = CrabCupsMega( [ 3, 8, 9, 1, 2, 5, 4, 6, 7 ], 9 )
    print( game )
    #game.playRound()
    #print(game)
    #return
    for i in range(10):
        game.playRound()
        print(game)
    for i in range(90):
        game.playRound()
    print(game)
    
test()

game = CrabCupsMega( [2,1,9,7,4,8,3,6,5], 1000000 )
print('Game initialized with 1000000 cups')
for i in range(100):
    for j in range(100000):
        game.playRound()
    print('.', end='')

game.PresentResult()