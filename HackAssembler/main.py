import re


class Assembler:
    def file_manager(self):
        pass

    def whitespace_remover(self, document):
        uncommented = re.sub(r'(//[\S ]*)', '', document)
        de_whitespace = uncommented.replace(' ', '')
        no_empty_rows = [line for line in de_whitespace.split('\n') if line.strip() != '']
        return '\n'.join(no_empty_rows)

    def instruction_translator(self, line):

        def _a_instruction_translator(instruction):
            return '{0:016b}'.format(int(instruction.replace('@', '')))

        def _c_instruction_translator(instruction):
            component_table = [('D|A', '010101'), ('A\+1', '110111'), ('D&A', '000000'), ('D\+A', '000010'),
                               ('M\-1', '110010'), ('M\+1', '110111'), ('D&M', '000000'), ('A\-1', '110010'),
                               ('D\-M', '010011'), ('M-D', '000111'), ('M\+D', '000010'), ('D\|M', '010101'),
                               ('A\-D', '000111'), ('D\-1', '001110'), ('D\-A', '010011'), ('A\|D', '010101'),
                               ('1\+A', '110111'), ('A&D', '000000'), ('A\+D', '000010'), ('M&D', '000000'),
                               ('1\+D', '011111'), ('M\|D', '010101'), ('\-M', '110011'), ('!A', '110001'),
                               ('!M', '110001'), ('\-1', '111010'), ('1', '111111'), ('!D', '001101'),
                               ('\-A', '110011'), ('\-D', '001111'), ('D', '001100'), ('A', '110000'),
                               ('M', '110000'), ('0', '101010')]

            destination_table = [('MD', '011'), ('D', '010'), ('AMD', '111'), ('A', '100'), ('AM', '101'),
                                 ('AD', '110'), ('null', '000'), ('M', '001')]

            jump_table = [('JEQ', '010'), ('JGE', '011'), ('JLE', '110'), ('JLT', '100'), ('null', '000'),
                          ('JGT', '001'), ('JNE', '101'), ('JMP', '111')]

            split_instruction = instruction.replace('=', '*').replace(';', '*').split('*')
            destination = split_instruction[0]
            component = split_instruction[1]

            component_control = '0'
            if 'M' in component:
                component_control = '1'

            for i in destination_table:
                destination = re.sub(r'^{}$'.format(i[0]), i[1], destination)

            for i in component_table:
                component = re.sub(r'^{}$'.format(i[0]), i[1], component)
            try:
                jump = split_instruction[2]
                for i in jump_table:
                    jump = re.sub(r'^{}$'.format(i[0]), i[1], jump)
            except IndexError:
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
                for nr in range(1, 15):
                    variables.remove('@R{}'.format(nr))
            except ValueError:
                pass

            no_empty_variables = ['@{}'.format(i) for i in variables if i]

            memory_locations = ['@{}'.format((no_empty_variables.index(i) + 16)) for i in no_empty_variables]
            translation_table = dict(zip(no_empty_variables, memory_locations))
            translation_table['@SCREEN'] = '@16384'
            translation_table['@KBD'] = '@24576'
            # for nr in range(1, 15):
            #     indx = '@R{}'.format(nr)
            #     translation_table[indx] = "@{}".format((nr - 1))

            lines = document.split('\n')
            no_variable_document = lines

            for line in lines:
                for translation in translation_table:
                    if translation in line:
                        no_variable_document[lines.index(line)] = translation_table[translation]

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
        no_whitespace = self.whitespace_remover(document_string)
        no_symbols = self.symbol_translator(no_whitespace)
        instruction_list = no_symbols.split('\n')
        machine_code_instructions = [self.instruction_translator(instruction) for instruction in instruction_list]
        return machine_code_instructions


a = Assembler()
print(a.symbol_translator('''@R2
M=0
@R1
D=M
@counter
M=D
(Loop)
@R1
D=M
@Negative
D;JLT
@Endless
D;JEQ
@R0
D=M
@R2
M=M+D
@counter
M=M-1
D=M
@Loop
D;JGT
@Endless
D;JEQ
(Negative)
@R0
D=M
@R2
M=M-D
@counter
M=M+1
D=M
@Loop
D;JLT
@Endless
D;JEQ
@Endless
(Endless)
0;JMP'''))
