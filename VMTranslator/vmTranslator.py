import re
import sys
from itertools import chain


class Parser:
    ''' Takes .vm file and parses it into instructions. '''
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
        self.call_count = 0

    def main(self):
        self._bootstrap()
        self.parse_result = Parser().main()
        self.instructions = self.parse_result[0]
        self.filename = self.parse_result[1]
        for instruction in self.instructions:
            self.instruction_type_separator(instruction)
        self._terminate()
        self.output()
        print('Finished successfully. Output file: "{}{}"'.format(self.filename, '.asm'))

    def _bootstrap(self):
        ''' Adds initialisation code for VM. '''
        self.instructions_assembly.extend(['@256', 'D=A', '@SP', 'M=D'])

    def _terminate(self):
        ''' Adds termination loop to avoid accessing unintended memory. '''
        self.instructions_assembly.extend(['(INFLOOP)', '@INFLOOP', '0;JMP'])

    def instruction_type_separator(self, instruction):
        '''Filters instruction into arithmetic, logical, memory, branching and functional.'''
        arg1 = instruction[0]
        if arg1 == 'pop' or arg1 == 'push':
            self.memory_translator(instruction)
        elif arg1 == 'add' or arg1 == 'sub' or arg1 == 'neg' or arg1 == 'and' or arg1 == 'or' or arg1 == 'not':
            self.arithmetic_translator(instruction)
        elif arg1 == 'eq' or arg1 == 'gt' or arg1 == 'lt':
            self.logical_translator(instruction)
        elif arg1 == 'label' or arg1 == 'goto' or arg1 == 'if-goto':
            self.branching_translator(instruction)
        elif arg1 == 'function' or arg1 == 'return' or arg1 == 'call':
            self.function_translator(instruction)
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

        docstring_1 = ['// {}']
        pop_from_stack = ['@SP', 'M=M-1', 'A=M', 'D=M']
        decrement_sp = ['@SP', 'M=M-1']
        increment_sp = ['@SP', 'M=M+1']
        set_a_to_stack = ['@SP', 'A=M']
        label_start = ['@JUMP{}'.format(self.jump_count)]
        label_end = ['@ENDJUMP{}'.format(self.jump_count)]
        assign_start = ['(JUMP{})'.format(self.jump_count)]
        assign_end = ['(ENDJUMP{})'.format(self.jump_count)]

        common_template = list(chain(docstring_1,
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
            self.instruction_translator(instruction=instruction, template=template, instruction_type='memory')
        elif arg0 == 'push':
            if arg1 == 'constant':
                load_from = ['D=A']
            else:
                load_from = ['D=M']
            template = list(chain(docstring_3,
                                  memory_segment_procedures,
                                  load_from,
                                  push_to_stack))
            self.instruction_translator(instruction=instruction, template=template, instruction_type='memory')
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

    def branching_translator(self, instruction):
        ''' Builds branching instruction template. '''
        arg1 = instruction[0]

        if arg1 == 'label':
            template = ['// {} {}', '({}${})']
            self.instruction_translator(instruction=instruction, template=template, instruction_type='branching')
        elif arg1 == 'goto':
            template = ['// {} {}', '@{}${}', '0;JMP']
            self.instruction_translator(instruction=instruction, template=template, instruction_type='branching')
        elif arg1 == 'if_goto':
            template = ['// {} {}', '@SP', 'AM=M-1', 'D=M', 'M=0', '@{}${}', 'D;JNE']
            self.instruction_translator(instruction=instruction, template=template, instruction_type='branching_if')
        else:
            Warning('Bad instruction -({})'.format(instruction))

    def function_translator(self, instruction):
        ''' Builds function instruction template. '''

        decrement_sp = ['@SP', 'M=M-1']
        push_to_stack = ['@SP', 'A=M', 'M=D', '@SP', 'M=M+1']

        if instruction[0] == 'function':
            push_empty_var = ['D=0', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']
            template = ['// {} {} {}', '({})']

            for _ in range(int(instruction[2])):
                template += push_empty_var

            self.instruction_translator(instruction=instruction, template=template, instruction_type='function')
        elif instruction[0] == 'call':
            ret = '@{}%ret.{}'.format(self.filename, self.call_count)
            self.call_count += 1

            push_state = [[i, 'D=M'].extend(push_to_stack) for i in ['@LCL', '@ARG', '@THIS', '@THAT']]

            setup_steps = str(5 + int(instruction[2]))
            function_address = '@{}'.format(instruction[1])
            return_address = '({})'.format(ret[1:])

            template = list(chain(['// {} {} {}', ret, 'D=A'],
                                  push_to_stack,
                                  push_state,
                                  ['@SP', '@D=M', '@LCL',
                                   'M=D', setup_steps,
                                   'D=D-A', '@ARG', 'M=D',
                                   function_address, '0;JMP',
                                   return_address]))

            self.instruction_translator(instruction=instruction, template=template, instruction_type='call')
        elif instruction[0] == 'return':
            frame = '@R13'
            ret = '@R14'
            push_state = []

            counter = 1
            for i in ['@THAT', '@THIS', '@ARG', '@LCL']:
                push_state.extend([frame, 'D=M', '@{}'.format(counter), 'D=D-A', 'A=D', 'D=M', i, 'M=D'])
                counter += 1

            template = list(chain(['// {}', '@LCL', 'D=M', frame, 'M=D',
                                   frame, 'D=M', '@5', 'D=D-A',
                                   'A=D', 'D=M', ret, 'M=D'],
                                  decrement_sp,
                                  ['A=M', 'D=M'],
                                  ['@ARG', 'A=M', 'M=D', '@ARG',
                                   'D=M', '@SP', 'M=D+1'],
                                  push_state,
                                  [ret, 'A=M', '0;JMP']))

            self.instruction_translator(instruction=instruction, template=template, instruction_type='return')

        else:
            Warning('Bad instruction -({})'.format(instruction))

    def instruction_translator(self, instruction, template, instruction_type='arithm/logic'):
        '''Takes the template provided and fits instructions into them.'''
        symbols = template

        if instruction_type == 'memory' or instruction_type == 'call':
            symbols[0] = symbols[0].format(instruction[0], instruction[1], instruction[2])
        elif instruction_type == 'arithm/logic' or instruction_type == 'return':
            symbols[0] = symbols[0].format(instruction[0])
        elif instruction_type == 'branching':
            symbols[0] = symbols[0].format(instruction[0])
            symbols[1] = symbols[1].format(self.filename, instruction[1])
        elif instruction_type == 'branching_if':
            symbols[0] = symbols[0].format(instruction[0])
            symbols[-2] = symbols[-2].format(self.filename, instruction[1])
        elif instruction_type == 'function':
            symbols[0] = symbols[0].format(instruction[0], instruction[1], instruction[2])
            symbols[1] = symbols[1].format(instruction[1])
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
