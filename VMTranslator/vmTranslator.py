import re
import sys


# // Pushes and adds two constants.
# push constant 7
# push constant 8
# add

class Parser:
    def __init__(self):
        self.arg1 = None
        self.arg2 = None
        self.location = None
        self.more_commands = False
        self.command_type = None
        self.document = None

        self.input()
        self.whitespace_remover()

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
        de_whitespace = uncommented.replace(' ', '')
        no_empty_rows = [line for line in de_whitespace.split('\n') if line.strip() != '']
        self.document = '\n'.join(no_empty_rows)

    def


if __name__ == '__main__':
    Parser()
