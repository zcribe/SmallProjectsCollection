import re
import sys


# // Pushes and adds two constants.
# push constant 7
# push constant 8
# add

class Parser:
    # Takes .vm file and parses it into instructions
    def __init__(self):
        self.filename = None
        self.document = None
        self.instructions = None

    def main(self):
        self.input()
        self.filename = sys.argv[1].split('.')[0]
        self.whitespace_remover()
        self.instruction_separator()
        return self.instructions, self.filename

    def input(self):
        try:
            with open(sys.argv[1], 'r') as file:
                self.document = file.read()
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
    # Takes the seperate instructions, translates, outputs .asm file
    def __init__(self):
        self.parse_result = None
        self.filename = None
        self.instructions = []
        self.instructions_assembly = []

    def main(self):
        self.parse_result = Parser().main()
        self.instructions = self.parse_result[0]
        self.filename = self.parse_result[1]
        for instruction in self.instructions:
            self.instruction_type_separator(instruction)
        self.output()

    def output(self):
        with open('{}.asm'.format(self.filename), 'w+') as file:
            file.write('\n'.join(self.instructions_assembly))

    def instruction_type_separator(self, instruction):
        arg1 = instruction[0]
        if arg1 == 'pop' or arg1 == 'push':
            self.memory_translator(instruction)
        elif arg1 == 'add' or arg1 == 'sub' or arg1 == 'neg' or arg1 == 'and' or arg1 == 'or' or arg1 == 'not':
            self.arithmetic_translator(instruction)
        elif arg1 == 'eq' or arg1 == 'gt' or arg1 == 'lt':
            self.logical_translator(instruction)
        else:
            Warning('Unable to seperate instruction -({})'.format(instruction))

    def instruction_translator(self, instruction, template, arg_count=1):
        symbols = template
        if arg_count == 3:
            symbols[0] = symbols[0].format(instruction[0], instruction[1], instruction[2])
            symbols[1] = symbols[1].format(instruction[2])
        elif arg_count == 1:
            symbols[0] = symbols[0].format(instruction[0])
        else:
            Warning('Wrong argument count -({})'.format(instruction))
        self.instructions_assembly.extend(symbols)

    def arithmetic_translator(self, instruction):
        arg1 = instruction[0]
        if arg1 == 'add':
            template = ['// {}', 'M=M+D']
            self.instruction_translator(instruction=instruction, template=template)
        elif arg1 == 'sub':
            template = ['// {}', 'M=M-D']
            self.instruction_translator(instruction=instruction, template=template)
        elif arg1 == 'and':
            template = ['// {}', 'M=M&D']
            self.instruction_translator(instruction=instruction, template=template)
        elif arg1 == 'or':
            template = ['// {}', 'M=M|D']
            self.instruction_translator(instruction=instruction, template=template)
        elif arg1 == 'not':
            template = ['// {}', 'M=!M']
            self.instruction_translator(instruction=instruction, template=template)
        else:
            Warning('Bad instruction -({})'.format(instruction))

    def logical_translator(self, instruction):
        arg1 = instruction[0]
        if arg1 == 'eq':
            template = ['// {}', 'D=M-D', 'D;JEQ']
            self.instruction_translator(instruction=instruction, template=template)
        elif arg1 == 'gt':
            template = ['// {}', 'D=M-D', 'D;JGT']
            self.instruction_translator(instruction=instruction, template=template)
        elif arg1 == 'lt':
            template = ['// {}', 'D=M-D', 'D;JLT']
            self.instruction_translator(instruction=instruction, template=template)
        else:
            Warning('Bad instruction -({})'.format(instruction))

    def memory_translator(self, instruction):
        if instruction[0] == 'pop':
            template = ['// {} {} {}', '@SP', 'D=M', ]
            self.instruction_translator(instruction=instruction, template=template, arg_count=3)
        elif instruction[0] == 'push':
            # Push
            template = ['// {} {} {}', '@{}', 'D=A', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']
            self.instruction_translator(instruction=instruction, template=template, arg_count=3)
        else:
            Warning('Bad instruction -({})'.format(instruction))

    def memory_segment_procedures(self, segment):
        pass



if __name__ == '__main__':
    a = CodeWriter()
    a.main()
