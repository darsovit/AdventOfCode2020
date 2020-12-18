#!python

import re

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))

class TicketRuleFinder:
    def __init__(self):
        self.ranges = {}
        self.rules  = {}
        self.rulesRE = re.compile(r'(?P<name>[^:]+): (?P<firstrangemin>\d+)-(?P<firstrangemax>\d+) or (?P<secondrangemin>\d+)-(?P<secondrangemax>\d+)$')

    def readRule(self, line):
        match = self.rulesRE.match(line)
        if match is None:
            return False
        name = match['name']
        firstrange = ( int(match['firstrangemin']), int(match['firstrangemax']) )
        secondrange = ( int(match['secondrangemin']), int(match['secondrangemax']) )
        self.rules[name] = ( firstrange,secondrange )
        self.ranges[firstrange] = name
        self.ranges[secondrange] = name
        return True
        
    def scanForInvalidValues(self, ticket):
        for value in ticket.getValues():
            valid = False
            for range in self.ranges:
                if ( value >= range[0] and value <= range[1] ):
                    valid = True
                    break
            if not valid:
                yield value

    def __repr__(self):
        return '{{rules: {}, ranges: {}}}'.format(self.rules, self.ranges)
    
    def GetPossibleTypes( self, value ):
        possibleTypes = set()
        for range in self.ranges:
            if ( value >= range[0] and value <= range[1] ):
                possibleTypes.add( self.ranges[range] )
        return possibleTypes

    def FindIndexWithOneType(indexToTypes):
        foundTypeToIndex = {}
        for index in indexToTypes:
            if len(indexToTypes[index]) == 1:
                type = list(indexToTypes[index])[0]
                assert type not in foundTypeToIndex, 'Type {} already set for index {}, now found: {}'.format(type, foundTypeToIndex[type], index)
                foundTypeToIndex[type] = index
        return foundTypeToIndex

    def FindTypesInOneIndex(possibleTypesForIndex):
        mapTypesToIndices = {}
        # First build the possible types to index set
        for index in possibleTypesForIndex:
            for type in possibleTypesForIndex[index]:
                if type not in mapTypesToIndices:
                    mapTypesToIndices[type] = set()
                mapTypesToIndices[type].add(index)
        foundTypeToIndex = {}
        for mapType in mapTypesToIndices:
            if len(mapTypesToIndices[mapType]) == 1:
                foundTypeToIndex[mapType] = list(mapTypesToIndices[mapType])[0]
        return foundTypeToIndex
            
    def FindValidRulesPerValueLine(self, tickets):
        possibleTypesForIndex = {}
        for ticket in tickets:
            for (count,value) in enumerate(ticket.getValues()):
                setOfPossibleTypes = self.GetPossibleTypes( value )
                if count not in possibleTypesForIndex:
                    possibleTypesForIndex[count] = setOfPossibleTypes
                else:
                    possibleTypesForIndex[count] = possibleTypesForIndex[count].intersection( setOfPossibleTypes )
        
        changeFound = True
        foundIndexWithType = {}
        count = 0
        while changeFound:
            count += 1
            print( '******************* Reduction phase {} ************************************'.format(count) )

            changeFound = False
            foundTypeWithIndex = TicketRuleFinder.FindIndexWithOneType(possibleTypesForIndex)
            foundTypesWithOneIndex = TicketRuleFinder.FindTypesInOneIndex(possibleTypesForIndex)
            print('foundTypeWithIndex:', foundTypeWithIndex)
            print('foundTypesWithOneIndex:', foundTypesWithOneIndex)
            if len(foundTypeWithIndex) > 0:
                changeFound = True
                for type in foundTypeWithIndex:
                    typeIndex = foundTypeWithIndex[type]
                    foundIndexWithType[typeIndex] = type
                    del possibleTypesForIndex[typeIndex]
                    for index in possibleTypesForIndex:
                        if type in possibleTypesForIndex[index]:
                            possibleTypesForIndex[index].remove(type)
            if len(foundTypesWithOneIndex) > 0:
                changeFound = True
                for type in foundTypesWithOneIndex:
                    typeIndex = foundTypesWithOneIndex[type]
                    if typeIndex in foundIndexWithType:
                        assert foundIndexWithType[typeIndex] == type, '{} != {}'.format(foundIndexWithType[typeIndex], type)
                        assert typeIndex not in possibleTypesForIndex
                    else:
                        foundIndexWithType[typeIndex] = type
                        del possibleTypesForIndex[typeIndex]
            print( 'foundIndexWithType:', foundIndexWithType )
            print( 'possibleTypesForIndex:', possibleTypesForIndex )
        
                
                    
                    
        return (foundIndexWithType,possibleTypesForIndex)

class Ticket:
    def __init__(self):
        self.values = []

    def readTicket(self, line):
        self.values = list(map(int, line.split(',')))
    
    def getValues(self):
        return self.values

    def __repr__(self):
        return '{{values: {}}}'.format(self.values)

def handleInput(input):
    ticketRuleFinder = TicketRuleFinder()
    yourTicket  = Ticket()
    nearbyTickets = []
    parsing = 'rules'
    for line in input:
        if parsing == 'rules':
            if not ticketRuleFinder.readRule( line ):
                parsing = None
        elif parsing == 'your ticket':
            yourTicket.readTicket( line )
            parsing = None
        elif parsing == 'nearby tickets':
            nearbyTicket = Ticket()
            nearbyTicket.readTicket(line)
            nearbyTickets += [ nearbyTicket ]
        else:
            assert parsing is None, 'Out of acceptable states but parsing is not None: {}'.format(parsing)
            if line == 'your ticket:':
                parsing = 'your ticket'
            elif line == 'nearby tickets:':
                parsing = 'nearby tickets'
            else:
                assert line == '', 'In-between states and not a blank line: {}'.format(line)
    return (ticketRuleFinder,yourTicket,nearbyTickets)    
    
#print(ticketRules)
#print(yourTicket)
#print(nearbyTickets)
input = readInput()
(ticketRuleFinder,myTicket,nearbyTickets) = handleInput(input)




validTickets = []
for nearbyTicket in nearbyTickets:
    hasInvalidEntries = False
    for invalidValue in ticketRuleFinder.scanForInvalidValues(nearbyTicket):
        hasInvalidEntries = True
    if not hasInvalidEntries:
        validTickets += [ nearbyTicket ]

(foundIndexWithType,possibleTypesForIndex) = ticketRuleFinder.FindValidRulesPerValueLine( validTickets )
print(foundIndexWithType)

answer = 1
for index in foundIndexWithType:
    if 'departure' in foundIndexWithType[index]:
        value = myTicket.getValues()[index]
        answer *= value
        print( '* {} = {}'.format(value, answer))

print(answer)