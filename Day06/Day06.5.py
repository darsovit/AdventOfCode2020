#!python

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))

def buildGroupAnswer( input ):
    groupAnswer = None
    groupCount  = 0
    personCount = 0
    for line in input:
        if len(line) == 0:
            #print( 'groupAnswer {}: {}'.format(groupCount, groupAnswer ) )
            yield groupAnswer
            groupAnswer = None
            groupCount  += 1
            personCount = 0
        else:
            personCount += 1
            person = set(line)
            #print('\tgroup {}, person {}: {}'.format(groupCount,personCount, person))
            if groupAnswer is None:
                groupAnswer = person
            else:
                groupAnswer = groupAnswer.intersection( person )
            #print('\tgroup {} after {} people: {}'.format(groupCount, personCount, groupAnswer) )
    #print('\tgroupAnswer {}: {}'.format(groupCount, groupAnswer) )
    yield groupAnswer

count = 0    
for groupAnswer in buildGroupAnswer( readInput() ):
    count += len( groupAnswer )

print( count )