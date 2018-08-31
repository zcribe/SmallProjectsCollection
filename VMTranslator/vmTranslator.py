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
        print(self.instructions)


if __name__ == '__main__':
    a = Parser()
    a.main()
