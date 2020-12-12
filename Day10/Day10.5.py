#! python

def readInput():
    with open('input.txt') as f:
        return list(map(int, f.readlines()))


def testInput():
    return [16,10,15,5,1,11,7,19,6,12,4]

def testInput2():
    return [28,33,18,42,31,14,46,20,48,47,24,23,49,45,19,38,39,11,1,32,25,35,8,17,7,9,4,2,34,10,3]

input = readInput()
input.sort()

current = 0
difference_1 = 0
difference_2 = 0
difference_3 = 0

differences = []
for adapter in input:
    differences += [adapter - current]
    current = adapter



groups = [[]]
for difference in differences:
    if difference < 3:
        groups[-1] += [ difference ]
    else:
        assert 3 == difference, 'Difference ({}) greater than 3'.format(difference)
        groups += [ [] ]

print(input)        
print(differences)
print(groups)

def calcCombos( group ):
    if [1,1] == group:   # The last must always be there, the first can be skipped or not
        return 2
    if [1,1,1] == group: # The last must always be there, either of the first two can be skipped
        return 4
    if [1,1,1,1] == group: # Consider: (0),1,2,3,4,(7) -- the 4 must remain and at least one of the others [1,2,3] must be there: [1,2,3],[1,2],[1,3],[2,3],[1],[2],[3]
        return 7
    assert group == [1] or group == [], 'Unknown group combo {}'.format( group )
    return 1

combos = 1

for group in groups:
    this_group = calcCombos( group )
    combos = combos * this_group
    print( this_group, combos )
print( combos )