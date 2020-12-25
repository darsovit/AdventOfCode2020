#!python

def readInput():
    with open('input.txt') as f:
        return list(map(int, f.readlines()))

def determineLoop(subject, publicKey):
    done = False
    count = 0
    value = 1
    while not done:
        count += 1
        value = (value*subject) % 20201227
        done = (value == publicKey)
    return count
    

def calculateEncryptionKey(subject, count):
    value = 1
    for i in range(count):
        value = (value * subject) % 20201227
    return value

input = readInput()
print( calculateEncryptionKey(input[1], determineLoop(7, input[0])) )
print( calculateEncryptionKey(input[0], determineLoop(7, input[1])) )