#!python

class CrabCups:
    def __init__(self, start):
        self.state = start
        self.rounds = 0

    def __nextLower(aChar):
        if aChar == '1':
            return '9'
        return chr(ord(aChar)-1)

    def playRound(self):
        saved_cups = self.state[1:4]
        interstate = self.state[:1] + self.state[4:]
        findvalue = CrabCups.__nextLower(self.state[0])
        pos = interstate.find(findvalue)
        while pos is -1:
            findvalue = CrabCups.__nextLower(findvalue)
            pos = interstate.find(findvalue)
        #print('found: {} in {} at pos {}'.format(findvalue,interstate,pos))
        assert pos != 0, 'Next lower from {} should not be {} at pos 0, state= {}'.format(self.state[0], findvalue, self.state)
        self.state = interstate[1:pos+1] + saved_cups + interstate[pos+1:] + interstate[0]
        self.rounds += 1
            
    def __repr__(self):
        return '{{rounds: {}, state: {}}}'.format( self.rounds, self.state )

def test():
    game = CrabCups( '389125467' )
    print(game)
    for i in range(10):
        game.playRound()
        print(game)
    for i in range(90):
        game.playRound()
    print(game)
    
    
test()
game = CrabCups( '219748365' )
for i in range(100):
    game.playRound()

print(game)