#! python

import re

noop_re     = re.compile(r'^nop (?P<posneg>[-+])(?P<count>\d+)')
acc_re      = re.compile(r'^acc (?P<posneg>[-+])(?P<count>\d+)')
jmp_re      = re.compile(r'^jmp (?P<posneg>[-+])(?P<count>\d+)')

def readInput():
    with open('input.txt') as f:
        return list(map(str.rstrip, f.readlines()))

class Computer:
    def __init__(self, lines):
        self.program     = lines
        self.pc          = 0
        self.accumulator = 0
        self.cmds        = [ ( noop_re, self.noop ), ( acc_re, self.acc ), ( jmp_re, self.jmp ) ]

    def noop(self, match):
        return 1

    def acc(self, match):
        if match['posneg'] == '+':
            self.accumulator += int(match['count'])
        else:
            assert match['posneg'] == '-'
            self.accumulator -= int(match['count'])
        return 1

    def jmp(self, match):
        if match['posneg'] == '+':
            return int(match['count'])
        assert match['posneg'] == '-', match
        return -1*int(match['count'])

    def run_instruction(self, instruction):
        for cmd in self.cmds:
            match = cmd[0].match(instruction)
            if match is not None:
                return cmd[1]( match )
        assert False, 'should always find our command'
        
    def step(self):
        instruction = self.program[self.pc]
        pc_step = self.run_instruction( instruction )
        self.pc += pc_step
        return self.pc

    def __str__(self):
        return 'Computer(pc:{}, accumulator:{})'.format(self.pc, self.accumulator)

    def __repr__(self):
        return('{program:'+self.program+', pc:'+self.pc+', accumulator:'+self.accumulator+'}')

    def complete(self):
        return self.pc == len(self.program)

    def crashed(self):
        return self.pc > len(self.program)


def testTranslatedProgram( input, lineReplaced, newline ):
    computer = Computer( input[:lineReplaced] + [newline] + input[lineReplaced+1:] )
    run_instructions = set()
    run_instructions.add( 0 )

    not_repeated = True
    while not_repeated and not computer.complete() and not computer.crashed():
        new_pc = computer.step()
        if new_pc in run_instructions:
            not_repeated = False
        else:
            run_instructions.add(new_pc)
    if computer.complete():
        print( 'COMPLETE with {} with {}: {}'.format(lineReplaced, newline, computer) )
        return True
    elif computer.crashed():
        print( 'CRASH with {} with {}: {}'.format(lineReplaced, newline, computer) )
        return False
    else:
        assert not not_repeated
        print( 'Infinite Loop with {} with {}: {}'.format(lineReplaced, newline, computer) )
        return False

def testJmpToNopPrograms( input ):
    for i in range(0,len(input)):
        match = jmp_re.match(input[i])
        if match:
            if testTranslatedProgram( input, i, 'nop {}{}'.format(match['posneg'], match['count']) ):
                return True
    return False

program = readInput()

testJmpToNopPrograms(program)