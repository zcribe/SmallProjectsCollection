import re
import sys


# // Pushes and adds two constants.
# push constant 7
# push constant 8
# add

class Parser:
    def __init__(self):
        self.document = None
        self.instructions = None

    def main(self):
        self.input()
        self.whitespace_remover()
        self.instruction_separator()
        return self.instructions

    def input(self):
        try:
            with open(sys.argv[1], 'r') as f:
                self.document = f.read()
        except FileNotFoundError:
            raise Warning('{} was not found'.format(sys.argv[1]))
        except IndexError:
            raise Warning('File argument not supplied. Usage: vmTranslator FILENAME')

    def whitespace_remover(self):
        document = self.document
        uncommented = re.sub(r'(//[\S ]*)', '', document)
        no_empty_rows = [line for line in uncommented.split('\n') if line.strip() != '']
        self.instructions = no_empty_rows

    def instruction_separator(self):
        seperated_instructions = []
        for instruction in self.instructions:
            seperated_instructions.append(instruction.split(' '))
        self.instructions = seperated_instructions


class CodeWriter:
    def __init__(self):
        self.instructions = []
        self.instructions_assembly = []

    def main(self):
        self.instructions = Parser().main()
        for instruction in self.instructions:
            self.instruction_type_separator(instruction)

    def output(self):
        pass

    def instruction_type_separator(self, instruction):
        arg1 = instruction[0]
        if arg1 == 'pop' or arg1 == 'push':
            self.memory_translator(instruction)
        elif arg1 == 'add' or arg1 == 'sub' or arg1 == 'neg':
            self.arithmetic_translator(instruction)
        elif arg1 == 'eq' or arg1 == 'gt' or arg1 == 'lt' or arg1 == 'and' or arg1 == 'or' or arg1 == 'not':
            self.logical_translator(instruction)

    def memory_translator(self, instruction):
        arg1 = instruction[1]
        arg2 = instruction[2]
        if arg1 == 'pop':
            self.instructions_assembly.extend(None)
        else:
            push = ['// push {} {}', '@{}', 'D=A', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']
            push[0] = push[0].format(arg1, arg2)
            push[1] = push[1].format(arg2)
            self.instructions_assembly.extend(push)

    def arithmetic_translator(self, instruction):
        if instruction[0] == 'add':
            self.instructions_assembly.extend(None)
        elif instruction[0] == 'sub':
            self.instructions_assembly.extend(None)
        else:
            self.instructions_assembly.extend(None)

    def logical_translator(self, instruction):
        arg1 = instruction[0]
        if arg1 == 'eq':
            self.instructions_assembly.extend(None)
        elif arg1 == 'gt':
            self.instructions_assembly.extend(None)
        elif arg1 == 'lt':
            self.instructions_assembly.extend(None)
        elif arg1 == 'and':
            self.instructions_assembly.extend(None)
        elif arg1 == 'or':
            self.instructions_assembly.extend(None)
        else:
            self.instructions_assembly.extend(None)


if __name__ == '__main__':
    a = Parser()
    a.main()
