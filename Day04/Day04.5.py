#!python
import re

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
            'hcl:#cfa07d eyr:2025 pid:166559648',
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

def validateYear( passport, key, min, max ):
    return key in passport and int(passport[key]) >= min and int(passport[key]) <= max

def validateHeight( passport ):
    if 'hgt' not in passport:
        return False
    if passport['hgt'][-2:] == 'cm':
        cmHgt = int(passport['hgt'][:-2])
        return cmHgt >= 150 and cmHgt <= 193
    elif passport['hgt'][-2:] == 'in':
        inHgt = int(passport['hgt'][:-2])
        return inHgt >= 59 and inHgt <= 76
    return False

haircolorre = re.compile(r'^#[0-9a-f]{6}$')

def validateHairColor(passport):
    if 'hcl' not in passport:
        return False
    return haircolorre.match(passport['hcl']) is not None

def validateEyeColor(passport):
    if 'ecl' not in passport:
        return False
    color = passport['ecl']
    return color in ('amb','blu','brn','gry','grn','hzl','oth')

passportre = re.compile(r'^\d{9}$')
def validatePassportId(passport):
    if 'pid' not in passport:
        return False
    return passportre.match(passport['pid']) is not None

def validatePassport( passport ):
    validBirthYear = validateYear(passport, 'byr', 1920, 2002)
    validIssueYear = validateYear(passport, 'iyr', 2010, 2020)
    validExpireYear = validateYear(passport, 'eyr', 2020, 2030)
    validHeight     = validateHeight(passport)
    validHairColor  = validateHairColor(passport)
    validEyeColor   = validateEyeColor(passport)
    validPassportId = validatePassportId(passport)
    if not validBirthYear:
        print('invalid birth year')
    if not validIssueYear:
        print('invalid issue year')
    if not validExpireYear:
        print('invalid expire year')
    if not validHeight:
        print('invalid height')
    if not validHairColor:
        print('invalid hair color')
    if not validEyeColor:
        print('invalid eye color')
    if not validPassportId:
        print('invalid passport id')
    return ( validBirthYear and validIssueYear and validExpireYear and validHeight and validHairColor and validEyeColor and validPassportId )

def testValidateYear():
    for i in range(1920,2003):
        assert validateYear({'byr':i},'byr',1920,2002), i
    for i in range(1900,1920):
        assert not validateYear({'byr':i},'byr',1920,2002), i
    for i in range(2003,2020):
        assert not validateYear({'byr':i},'byr',1920,2002), i

def testValidateHeight():
    for i in range(59,77):
        assert validateHeight({'hgt':'{}in'.format(i)}), i
    for i in range(50,59):
        assert not validateHeight({'hgt':'{}in'.format(i)}), i
    for i in range(77,80):
        assert not validateHeight({'hgt':'{}in'.format(i)}), i
    for i in range(150,194):
        assert validateHeight({'hgt':'{}cm'.format(i)}), i
    for i in range(194,200):
        assert not validateHeight({'hgt':'{}cm'.format(i)}), i
    for i in range(140,150):
        assert not validateHeight({'hgt':'{}cm'.format(i)}), i

def testValidateHairColor():
    validHairColors = ['#123abc','#ffffff']
    invalidHairColors = ['123abc','#fffffg','#fffffff']
    for color in validHairColors:
        assert validateHairColor({'hcl':color}), color
    for color in invalidHairColors:
        assert not validateHairColor({'hcl':color}), color

def testValidateEyeColor():
    validEyeColors = ['amb','blu','brn','gry','grn','hzl','oth']
    invalidEyeColors = ['amz','am','bl','br','gr','green','grne']
    for color in validEyeColors:
        assert validateEyeColor({'ecl':color}),color
    for color in invalidEyeColors:
        assert not validateEyeColor({'ecl':color}),color

testValidateYear()
testValidateHeight()
testValidateHairColor()
testValidateEyeColor()

count = 0
for passport in generatePassport(readInput()):

    if validatePassport( passport ):
        print('valid:', passport)
        count += 1
    else:
        print('invalid:', passport)


print(count)