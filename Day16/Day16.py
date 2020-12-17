#!python

import re

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))

class TicketRules:
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

class Ticket:
    def __init__(self):
        self.values = []

    def readTicket(self, line):
        self.values = list(map(int, line.split(',')))
    
    def getValues(self):
        return self.values

    def __repr__(self):
        return '{{values: {}}}'.format(self.values)

input = readInput()
ticketRules = TicketRules()
yourTicket  = Ticket()
nearbyTickets = []
parsing = 'rules'
for line in input:
    if parsing == 'rules':
        if not ticketRules.readRule( line ):
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
        
    
#print(ticketRules)
#print(yourTicket)
#print(nearbyTickets)

sumInvalidValues = 0
for nearbyTicket in nearbyTickets:
    for invalidValue in ticketRules.scanForInvalidValues(nearbyTicket):
        sumInvalidValues += invalidValue
print(sumInvalidValues)