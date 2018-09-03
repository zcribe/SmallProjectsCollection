import re
import sys
from itertools import chain


class Parser:
    '''# Takes .vm file and parses it into instructions.'''
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
        '''Takes in .vm file.'''
        try:
            with open(sys.argv[1], 'r') as file:
                self.document = file.read()
        except FileNotFoundError:
            raise Warning('{} was not found'.format(sys.argv[1]))
        except IndexError:
            raise Warning('File argument not supplied. Usage: vmTranslator FILENAME')

    def whitespace_remover(self):
        '''De-comments and removes whitespace from input.'''
        document = self.document
        uncommented = re.sub(r'(//[\S ]*)', '', document)
        no_empty_rows = [line for line in uncommented.split('\n') if line.strip() != '']
        self.instructions = no_empty_rows

    def instruction_separator(self):
        '''Break instruction into segments'''
        seperated_instructions = []
        for instruction in self.instructions:
            seperated_instructions.append(instruction.split(' '))
        self.instructions = seperated_instructions


class CodeWriter:
    '''Takes the seperate instructions, translates, outputs .asm file.'''
    def __init__(self):
        self.parse_result = None
        self.filename = None
        self.instructions = []
        self.instructions_assembly = []
        self.jump_count = 0

    def main(self):
        self.parse_result = Parser().main()
        self.instructions = self.parse_result[0]
        self.filename = self.parse_result[1]
        for instruction in self.instructions:
            self.instruction_type_separator(instruction)
        self.output()

    def instruction_type_separator(self, instruction):
        '''Filters instruction into arithmetic, logical, memory.'''
        arg1 = instruction[0]
        if arg1 == 'pop' or arg1 == 'push':
            self.memory_translator(instruction)
        elif arg1 == 'add' or arg1 == 'sub' or arg1 == 'neg' or arg1 == 'and' or arg1 == 'or' or arg1 == 'not':
            self.arithmetic_translator(instruction)
        elif arg1 == 'eq' or arg1 == 'gt' or arg1 == 'lt':
            self.logical_translator(instruction)
        else:
            Warning('Unable to seperate instruction -({})'.format(instruction))

    def arithmetic_translator(self, instruction):
        '''Builds arithmetic instruction translation template'''
        arg1 = instruction[0]

        docstring_1 = ['// {}']
        pop_from_stack = ['@SP', 'M=M-1', 'A=M', 'D=M']
        decrement_sp = ['@SP', 'M=M-1']
        increment_sp = ['@SP', 'M=M+1']
        set_a_to_stack = ['@SP', 'A=M']

        non_negative_template = list(chain(docstring_1,
                                           pop_from_stack,
                                           decrement_sp,
                                           set_a_to_stack,
                                           [],
                                           increment_sp))

        negative_template = list(chain(docstring_1,
                                       decrement_sp,
                                       set_a_to_stack,
                                       [],
                                       increment_sp))

        if arg1 == 'add':
            template = non_negative_template
            template[-2] = 'M=M+D'
            self.instruction_translator(instruction=instruction, template=template)
        elif arg1 == 'sub':
            template = non_negative_template
            template[-2] = 'M=M-D'
            self.instruction_translator(instruction=instruction, template=template)
        elif arg1 == 'and':
            template = non_negative_template
            template[-2] = 'M=M&D'
            self.instruction_translator(instruction=instruction, template=template)
        elif arg1 == 'or':
            template = non_negative_template
            template[-2] = 'M=M|D'
            self.instruction_translator(instruction=instruction, template=template)
        elif arg1 == 'not':
            template = negative_template
            template[-2] = 'M=!M'
            self.instruction_translator(instruction=instruction, template=template)
        elif arg1 == 'neg':
            template = negative_template
            template[-2] = 'M=-M'
            self.instruction_translator(instruction=instruction, template=template)
        else:
            Warning('Bad instruction -({})'.format(instruction))

    def logical_translator(self, instruction):
        '''Builds logical instruction translation template.'''
        arg1 = instruction[0]

        docstring_3 = ['// {} {} {}']
        pop_from_stack = ['@SP', 'M=M-1', 'A=M', 'D=M']
        decrement_sp = ['@SP', 'M=M-1']
        increment_sp = ['@SP', 'M=M+1']
        set_a_to_stack = ['@SP', 'A=M']
        label_start = ['@JUMP{}'.format(self.jump_count)]
        label_end = ['@ENDJUMP{}'.format(self.jump_count)]
        assign_start = ['(JUMP{})'.format(self.jump_count)]
        assign_end = ['(ENDJUMP{})'.format(self.jump_count)]

        common_template = list(chain(docstring_3,
                                     pop_from_stack,
                                     decrement_sp,
                                     set_a_to_stack,
                                     ['D=M-D'],
                                     label_start,
                                     [],
                                     set_a_to_stack,
                                     ['M=0'],
                                     label_end,
                                     ['0;JMP'],
                                     assign_start,
                                     set_a_to_stack,
                                     ['M=-1'],
                                     assign_end,
                                     increment_sp))
        self.jump_count += 1

        if arg1 == 'eq':
            template = common_template
            template[6] = 'D;JEQ'
            self.instruction_translator(instruction=instruction, template=template)
        elif arg1 == 'gt':
            template = common_template
            template[6] = 'D;JGT'
            self.instruction_translator(instruction=instruction, template=template)
        elif arg1 == 'lt':
            template = common_template
            template[6] = 'D;JLT'
            self.instruction_translator(instruction=instruction, template=template)
        else:
            Warning('Bad instruction -({})'.format(instruction))

    def memory_translator(self, instruction):
        '''Builds memory instruction translation template.'''
        arg0, arg1, arg2 = instruction
        memory_segment_procedures = self.memory_segment_procedures(arg1, arg2)

        docstring_3 = ['// {} {} {}']
        pop_from_stack = ['@SP', 'M=M-1', 'A=M', 'D=M']
        push_to_stack = ['@SP', 'A=M', 'M=D', '@SP', 'M=M+1']

        if arg0 == 'pop':
            template = list(chain(docstring_3,
                                  memory_segment_procedures,
                                  ['D=A', '@R13', 'M=D'],
                                  pop_from_stack,
                                  ['@R13', 'A=M', 'M=D']))
            self.instruction_translator(instruction=instruction, template=template, arg_count=2)
        elif arg0 == 'push':
            if arg1 == 'constant':
                load_from = ['D=A']
            else:
                load_from = ['D=M']
            template = list(chain(docstring_3,
                                  memory_segment_procedures,
                                  load_from,
                                  push_to_stack))
            self.instruction_translator(instruction=instruction, template=template, arg_count=2)
        else:
            Warning('Bad instruction -({})'.format(instruction))

    def memory_segment_procedures(self, segment, index):
        '''Adjusts template according to memory segment being operated on.'''
        if segment == 'constant':
            return ['@{}'.format(index)]
        elif segment == 'static':
            return ['@{}.{}'.format(self.filename, index)]
        elif segment == 'pointer':
            return ['@R{}'.format((3 + int(index)))]
        elif segment == 'temp':
            return ['@R{}'.format((5 + int(index)))]
        elif segment == 'local':
            return ['@LCL', 'D=M', '@{}'.format(index), 'A=D+A']
        elif segment == 'argument':
            return ['@ARG', 'D=M', '@{}'.format(index), 'A=D+A']
        elif segment == 'this':
            return ['@THIS', 'D=M', '@{}'.format(index), 'A=D+A']
        elif segment == 'that':
            return ['@THAT', 'D=M', '@{}'.format(index), 'A=D+A']
        else:
            Warning('Bad segment -({})'.format(segment))

    def instruction_translator(self, instruction, template, arg_count=1):
        '''Takes the template provided and fits instructions into them.'''
        symbols = template
        if arg_count == 3:
            symbols[0] = symbols[0].format(instruction[0], instruction[1], instruction[2])
            symbols[1] = symbols[1].format(instruction[2])
        elif arg_count == 2:
            symbols[0] = symbols[0].format(instruction[0], instruction[1], instruction[2])
        elif arg_count == 1:
            symbols[0] = symbols[0].format(instruction[0])
        else:
            Warning('Wrong argument count -({})'.format(instruction))
        self.instructions_assembly.extend(symbols)

    def output(self):
        '''Outputs assembly file with changed suffix.'''
        with open('{}.asm'.format(self.filename), 'w+') as file:
            file.write('\n'.join(self.instructions_assembly))


if __name__ == '__main__':
    initialised = CodeWriter()
    initialised.main()
