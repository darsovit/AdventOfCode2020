#! python

def readInput():
    with open('input.txt') as f:
        return list(map(int, f.readlines()))

def printPriors(priors):
    print('###################################################################')
    print('LENGTH of PRIORS:',len(priors))
    for prior in priors:
        print('length of possibles:',len(prior['possibles']))
        print(prior)

def addNumToPriors(num, priors):
    for prior in priors:
        prior['possibles'].add(prior['value']+num)
    priors += [{'value':num, 'possibles':set()}]
    #printPriors(priors)

def updatePriors(num, priors):
    priors.pop(0)
    addNumToPriors(num, priors)

def buildPreamble(nums):
    preambleSets = []
    for num in nums[0:25]:
        addNumToPriors(num, preambleSets)
    return preambleSets

def findNumInPriorSums(num, priors):
    for prior in priors:
        if num in prior['possibles']:
            return True
    return False

def findNumNotASumOfPriors(nums):
    priors = buildPreamble(nums[0:25])
    for num in nums[25:]:
        if not findNumInPriorSums(num, priors):
            return num
        else:
            updatePriors(num, priors)

def findConsecutiveNumsSumTo( magic, nums ):
    start = 0
    end   = 1
    value = nums[0]
    
    while value != magic:
        if value > magic:
            value -= nums[start]
            start += 1
        elif value < magic:
            value += nums[end]
            end += 1
    return (start, end)
    
nums = readInput()

magic_number = findNumNotASumOfPriors(readInput())

range_of_nums = findConsecutiveNumsSumTo( magic_number, nums )

min = magic_number
max = 0
for i in range( range_of_nums[0], range_of_nums[1] ):
    if nums[i] > max:
        max = nums[i]
    if nums[i] < min:
        min = nums[i]

print(range_of_nums)

print(nums[range_of_nums[0]:range_of_nums[1]])

print('sum of max and min:', max + min)