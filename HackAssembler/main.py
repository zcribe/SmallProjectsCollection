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
        screen_map_start_bit = '@16384'
        keyboard_map_start_bit = '@24576'
        pre_reserved_range = range(0, 16)
        pre_reserved_edge = pre_reserved_range[-1] + 1
        lines_document = document.split('\n')
        lines_document_cleaned = lines_document
        address_table = []
        variables = []
        labels = []

        for line in lines_document:
            if '@' in line:
                address_table.append(line)
            elif '(' in line:
                labels.append(line)
                address_table.append(line)

        for address in address_table:
            try:
                int(address[1:])
            except ValueError:
                variables.append(address)

        for variable in variables:
            for label in labels:
                if str(label[1:-1]) == str(variable[1:]):
                    variables.remove(variable)

        for variable in variables:
            if '(' in variable:
                variables[variables.index(variable)] = '@{}'.format(variable[1:-1])

        if '@SCREEN' in variables:
            variables.remove('@SCREEN')
        if '@KBD' in variables:
            variables.remove('@KBD')

        for nr in pre_reserved_range:
            current = '@R{}'.format(nr)
            if current in variables:
                variables.remove(current)

        variables = list(set(filter(None, variables)))
        definitions = ['@{}'.format((variables.index(i) + pre_reserved_edge)) for i in variables]
        translation_table = dict(zip(variables, definitions))

        translation_table['@SCREEN'] = screen_map_start_bit
        translation_table['@KBD'] = keyboard_map_start_bit
        for nr in pre_reserved_range:
            translation_table['@R{}'.format(nr)] = '@{}'.format(nr)
        for line in lines_document:
            for translation in translation_table:
                if translation == line:
                    lines_document_cleaned[lines_document.index(line)] = translation_table[translation]

        output = []
        for line in lines_document_cleaned:
            if ')' not in line:
                output.append(line)
        return '\n'.join(output)

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
    a.input_file()
