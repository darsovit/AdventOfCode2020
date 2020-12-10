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
    printPriors(priors)

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

print(findNumNotASumOfPriors(readInput()))
