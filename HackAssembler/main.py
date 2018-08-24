import re
import sys


class Assembler:
    def input_file(self):
        try:
            with open(sys.argv[1], 'r') as f:
                document = f.read()
            self.assemble_instructions(document)
        except FileNotFoundError:
            print('No such file "{}"'.format(sys.argv[1]))

    def output_file(self, output):
        with open('machine_code.hack', 'w+', encoding='utf8') as f:
            f.write(output)

    def whitespace_remover(self, document):
        uncommented = re.sub(r'(//[\S ]*)', '', document)
        de_whitespace = uncommented.replace(' ', '')
        no_empty_rows = [line for line in de_whitespace.split('\n') if line.strip() != '']
        return '\n'.join(no_empty_rows)

    def instruction_translator(self, line):

        def _a_instruction_translator(instruction):
            return '{0:016b}'.format(int(instruction.replace('@', '')))

        def _c_instruction_translator(instruction):
            component_table = [('D|A', '010101'), ('A+1', '110111'), ('D&A', '000000'), ('D+A', '000010'),
                               ('M-1', '110010'), ('M+1', '110111'), ('D&M', '000000'), ('A-1', '110010'),
                               ('D-M', '010011'), ('M-D', '000111'), ('M+D', '000010'), ('D+M', '000010'),
                               ('D|M', '010101'),
                               ('A-D', '000111'), ('D-1', '001110'), ('D-A', '010011'), ('A|D', '010101'),
                               ('1+A', '110111'), ('A&D', '000000'), ('A+D', '000010'), ('M&D', '000000'),
                               ('1+D', '011111'), ('D+1', '011111'), ('M|D', '010101'), ('-M', '110011'),
                               ('!A', '110001'),
                               ('!M', '110001'), ('-1', '111010'), ('!D', '001101'),
                               ('-A', '110011'), ('-D', '001111'), ('D', '001100'), ('A', '110000'),
                               ('M', '110000')]

            destination_table = [('MD', '011'), ('D', '010'), ('AMD', '111'), ('A', '100'), ('AM', '101'),
                                 ('AD', '110'), ('null', '000'), ('M', '001'), ('0', '000')]

            jump_table = [('JEQ', '010'), ('JGE', '011'), ('JLE', '110'), ('JLT', '100'), ('null', '000'),
                          ('JGT', '001'), ('JNE', '101'), ('JMP', '111')]

            jump_destination_table = [('M', '110000'), ('0', '101010'), ('A', '110000'), ('D', '001100')]

            split_instruction = instruction.replace('=', '*').replace(';', '*').split('*')
            destination = split_instruction[0]
            component = split_instruction[1]

            # TODO: Refactori spagetti kood

            component_control = '0'
            if '=' in instruction and ';' not in instruction and 'M' in component:
                component_control = '1'
            if ';' in instruction and 'M' in destination:
                component_control = '1'

            for i in destination_table:
                destination = re.sub(r'^{}$'.format(i[0]), i[1], destination)

            if component is '0':
                component = '101010'
            elif component is '1':
                component = '111111'
            else:
                for i in component_table:
                    component = component.replace(i[0], i[1])

            if ';' in instruction:
                jump = split_instruction[1]
                component = split_instruction[0]
                destination = '000'
                for i in jump_table:
                    jump = re.sub(r'^{}$'.format(i[0]), i[1], jump)
                for i in jump_destination_table:
                    component = re.sub(r'^{}$'.format(i[0]), i[1], component)
            else:
                jump = '000'

            return "".join(['111', component_control, component, destination, jump])

        if line[0] == "@":
            return _a_instruction_translator(line)
        else:
            return _c_instruction_translator(line)

    def symbol_translator(self, document):
        def variable_translator(document):
            variables = list(set(re.findall('@([A-Za-z]*)', document)))
            try:
                variables.remove('SCREEN')
                variables.remove('KBD')
                for nr in range(0, 15):
                    variables.remove('@R{}'.format(nr))
            except ValueError:
                pass

            no_empty_variables = ['@{}'.format(i) for i in variables if i]

            memory_locations = ['@{}'.format((no_empty_variables.index(i) + 16)) for i in no_empty_variables]
            translation_table = dict(zip(no_empty_variables, memory_locations))
            translation_table['@SCREEN'] = '@16384'
            translation_table['@KBD'] = '@24576'
            for nr in range(0, 15):
                translation_table['@R{}'.format(nr)] = "@{}".format(nr)

            lines = document.split('\n')
            no_variable_document = lines

            line_counter = 0
            for line in lines:
                for translation in translation_table:
                    if translation in line:
                        no_variable_document[line_counter] = translation_table[translation]
                line_counter += 1

            return '\n'.join(no_variable_document)

        def label_translator(document):
            labels = re.findall('\((.*?)\)', document)
            at_labels = ['@{}'.format(label) for label in labels]

            memory_locations = []
            lines = document.split('\n')

            # Find declarations, save line nrs, remove them
            [memory_locations.append(lines.index(line)) for line in lines if '(' in line]
            undeclared_document = [i for i in lines if not '(' in i]

            translation_table = dict(zip(at_labels, memory_locations))

            no_label_document = undeclared_document
            for line in undeclared_document:
                for translation in translation_table:
                    if translation in line:
                        no_label_document[undeclared_document.index(line)] = '@{}'.format(
                            translation_table[translation])

            return '\n'.join(no_label_document)

        no_label_document = label_translator(document)
        no_variable_document = variable_translator(no_label_document)

        return no_variable_document

    def assemble_instructions(self, document_string):
        print('Assembling...')
        no_whitespace = self.whitespace_remover(document_string)
        no_symbols = self.symbol_translator(no_whitespace)
        instruction_list = no_symbols.split('\n')
        machine_code_instructions = [self.instruction_translator(instruction) for instruction in instruction_list]
        self.output_file("\n".join(machine_code_instructions))
        print('Operation was successful')
        return "\n".join(machine_code_instructions)


if __name__ == '__main__':
    a = Assembler()
    # a.input_file()
    a.assemble_instructions('''// This file is part of www.nand2tetris.org
    // and the book "The Elements of Computing Systems"
    // by Nisan and Schocken, MIT Press.
    // File name: projects/06/add/Add.asm

    // Computes R0 = 2 + 3  (R0 refers to RAM[0])

    @2
    D=A
    @3
    D=D+A
    @0
    M=D
    ''')
