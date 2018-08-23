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

    def symbol_translator(self):
        pass

# print("Instr {}\n Pre={}\n CC={}\n Comp={}\n Dest={}\n JMP={}\n".format(instruction, '111', component_control, component, destination,  jump))
