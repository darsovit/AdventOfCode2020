#! python

def readInput():
    with open('input.txt') as f:
        return list(map(int, f.readlines()))

input = readInput()
input.sort()

current = 0
difference_1 = 0
difference_2 = 0
difference_3 = 0

for adapter in input:
    difference = adapter - current
    if difference == 1:
        difference_1 += 1
    elif difference == 2:
        difference_2 += 1
    elif difference == 3:
        difference_3 += 1
    else:
        assert False, '{} - {} = {}'.format( adapter, current, difference )
    current = adapter

difference_3 += 1

print( difference_1, difference_2, difference_3, 'answer:', difference_1 * difference_3 )

print(input)