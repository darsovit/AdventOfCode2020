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
    def __init__(self, input):
        self.playerdeck = []
        playerNo = None
        for line in input:
            if line.startswith('Player '):
                playerNo = int(line[len('Player '):-1])-1
                self.playerdeck += [[]]
                assert len(self.playerdeck) == playerNo+1,'Length of playerdeck ({}) is not equal to new playerNo {}'.format(len(self.playerdeck),playerNo+1)
            elif line != '':
                self.playerdeck[playerNo] += [int(line)]
        self.rounds = 0

    def __repr__(self):
        return '{{rounds: {}, playerdeck: {}}}'.format(self.rounds, self.playerdeck)

    def StepRound(self):
        player0 = self.playerdeck[0].pop(0)
        player1 = self.playerdeck[1].pop(0)
        if player0 > player1:
            self.playerdeck[0] += [ player0, player1 ]
        else:
            assert player1 > player0
            self.playerdeck[1] += [ player1, player0 ]
        self.rounds += 1
        
    def PlayGame(self):
        while (len(self.playerdeck[0]) > 0) and (len(self.playerdeck[1]) > 0):
            self.StepRound()

    def CalculateScore(self):
        winningPlayer = 0 if len(self.playerdeck[0]) > 0 else 1
        winningHand = self.playerdeck[winningPlayer].copy()
        winningHand.reverse()
        sum = 0
        for (count,card) in enumerate(winningHand, 1):
            sum += count * card
        return sum

war = War(readInput())
print(war)
war.PlayGame()

print(war)
print(war.CalculateScore())