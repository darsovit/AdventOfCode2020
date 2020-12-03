#!python

import re

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))


pattern = re.compile( r'(?P<min>\d+)-(?P<max>\d+) (?P<letter>\D): (?P<password>\D+)' )
def parseLine( line ):
    matches = re.match( pattern, line )
    return (int(matches['min']), int(matches['max']), matches['letter'], matches['password'])

def countLetterInPassword( password, letter ):
    count = 0
    for p in password:
        if letter == p:
            count += 1
    return count

def countValidPasswords(input):
    goodPasswords = 0
    for line in input:
        (min,max,letter,password) = parseLine( line )
        countOfLetterInPassword = countLetterInPassword( password, letter )
        if min <= countOfLetterInPassword and countOfLetterInPassword <= max:
            goodPasswords += 1
    return goodPasswords
    
print( countValidPasswords(readInput()) )