#!python

def testInput():
    return ['ecl:gry pid:860033327 eyr:2020 hcl:#fffffd',
            'byr:1937 iyr:2017 cid:147 hgt:183cm',
            '',
            'iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884',
            'hcl:#cfa07d byr:1929',
            '',
            'hcl:#ae17e1 iyr:2013',
            'eyr:2024',
            'ecl:brn pid:760753108 byr:1931',
            'hgt:179cm',
            '',
            'hcl:#cfa07d eyr:2025 pid:166559648'
            'iyr:2011 ecl:brn hgt:59in']
def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))

def buildPassport( line, passportParts ):
    parts = line.split(' ')
    for part in parts:
        (key,value) = part.split(':')
        passportParts[key]=value

def generatePassport(input):
    passportParts = dict()
    for line in input:
        if line == '':
            yield passportParts
            passportParts = dict()
        else:
            buildPassport( line, passportParts )
    yield passportParts

count = 0
for passport in generatePassport(readInput()):
    if 'byr' in passport and 'iyr' in passport and 'eyr' in passport and 'hgt' in passport and 'hcl' in passport and 'ecl' in passport and 'pid' in passport:
        count += 1
print(count)