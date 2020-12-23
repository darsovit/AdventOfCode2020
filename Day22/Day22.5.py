#! python

def testInput():
    return '''Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10'''.split('\n')

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))


class War:
    def __init__(self, depth, player0deck, player1deck):
        self.playerdeck = [ player0deck.copy(), player1deck.copy() ]
        self.depth      = depth
        self.rounds = 0
        self.states = set()

    def __repr__(self):
        return '{{depth: {}, rounds: {}, playerdeck: {}}}'.format(self.depth, self.rounds, self.playerdeck)

    def __awardCards(self, winner, player0, player1):
        self.rounds += 1
        if winner == 1:
            self.playerdeck[0] += [ player0, player1 ]
        else:
            assert winner == 2
            self.playerdeck[1] += [ player1, player0 ]
        #print(self)

    def __determineRecursiveWinner(self, player0cardCount, player1cardCount):
        nextWar = War( self.depth+1, self.playerdeck[0][:player0cardCount], self.playerdeck[1][:player1cardCount] )
        return nextWar.PlayGame()

    def __stateAlreadyExisted(self):
        # build current state,
        currentstate = ( tuple(self.playerdeck[0]), tuple(self.playerdeck[1]) )
        if currentstate in self.states:
            return True
        else:
            self.states.add(currentstate)
            return False
        assert len(self.states) == self.rounds, '{}'.format(self)

    def StepRound(self):
        player0 = self.playerdeck[0].pop(0)
        player1 = self.playerdeck[1].pop(0)
        recursiveWinner = None
        if len(self.playerdeck[0]) >= player0 and len(self.playerdeck[1]) >= player1:
            winner = self.__determineRecursiveWinner( player0, player1 )
            self.__awardCards( winner, player0, player1 )
        elif player0 > player1:
            self.__awardCards( 1, player0, player1 )
        else:
            assert player1 > player0, '{} > {} was false'.format(player1, player0)
            self.__awardCards( 2, player0, player1 )

    def PlayGame(self):
        while (len(self.playerdeck[0]) > 0) and (len(self.playerdeck[1]) > 0):
            if self.__stateAlreadyExisted():
                return 1
            self.StepRound()
        if len(self.playerdeck[0]) > 0:
            assert len(self.playerdeck[1]) == 0
            return 1
        else:
            return 2

    def CalculateScore(self):
        winningPlayer = 0 if len(self.playerdeck[0]) > 0 else 1
        winningHand = self.playerdeck[winningPlayer].copy()
        winningHand.reverse()
        sum = 0
        for (count,card) in enumerate(winningHand, 1):
            sum += count * card
        return sum

def buildWar(input):
    playerdeck = []
    playerNo = None
    for line in input:
        if line.startswith('Player '):
            playerNo = int(line[len('Player '):-1])-1
            playerdeck += [[]]
            assert len(playerdeck) == playerNo+1,'Length of playerdeck ({}) is not equal to new playerNo {}'.format(len(self.playerdeck),playerNo+1)
        elif line != '':
            playerdeck[playerNo] += [int(line)]
    return War(0, playerdeck[0], playerdeck[1])
    

war = buildWar(readInput())
print(war)
war.PlayGame()

print(war)
print(war.CalculateScore())