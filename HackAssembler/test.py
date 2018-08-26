import unittest

from .main import Assembler
from .sample_strings import *


class TestInstructionTranslator(unittest.TestCase):
    def test_c_instructions(self):
        a = Assembler()
        self.assertEqual(a.instruction_translator('M=0'), '1110101010001000')
        self.assertEqual(a.instruction_translator('D=M'), '1111110000010000')
        self.assertEqual(a.instruction_translator('M=M+D'), '1111000010001000')
        self.assertEqual(a.instruction_translator('AMD=A&D'), '1110000000111000')
        self.assertEqual(a.instruction_translator('M=A-D'), '1110000111001000')
        self.assertEqual(a.instruction_translator('M=!M'), '1111110001001000')
        self.assertEqual(a.instruction_translator('M=1'), '1110111111001000')
        self.assertEqual(a.instruction_translator('D=A|D'), '1110010101010000')
        self.assertEqual(a.instruction_translator('M=-M'), '1111110011001000')
        self.assertEqual(a.instruction_translator('D;JEQ'), '1110001100000010')
        self.assertEqual(a.instruction_translator('D;JGT'), '1110001100000001')
        self.assertEqual(a.instruction_translator('D;JLT'), '1110001100000100')
        self.assertEqual(a.instruction_translator('0;JMP'), '1110101010000111')
        self.assertEqual(a.instruction_translator('M;JGT'), '1111110000000001')
        self.assertEqual(a.instruction_translator('A;JGT'), '1110110000000001')
        self.assertEqual(a.instruction_translator('D=A'), '1110110000010000')

    def test_a_instructions(self):
        a = Assembler()
        self.assertEqual(a.instruction_translator('@1'), '0000000000000001')
        self.assertEqual(a.instruction_translator('@12'), '0000000000001100')
        self.assertEqual(a.instruction_translator('@234'), '0000000011101010')
        self.assertEqual(a.instruction_translator('@1532'), '0000010111111100')


class TestWhiteSpaceRemover(unittest.TestCase):
    def test_whitespace_remover(self):
        a = Assembler()
        self.assertEqual(a.whitespace_remover(test_string_one), whitespace_result_string_one)
        self.assertEqual(a.whitespace_remover(test_string_two), whitespace_result_string_two)


class TestInstructionSequence(unittest.TestCase):
    def sequence_helper(self, instructions, machine_code):
        a = Assembler()
        string = a.whitespace_remover(instructions)
        lines = string.split('\n')
        control = machine_code.split('\n')
        test = zip(lines, control)
        for i, v in test:
            self.assertEqual(a.instruction_translator(i), v)

    def test_sequences(self):
        self.sequence_helper(test_string_three_add_symboless, machine_code_three_add)
        self.sequence_helper(test_string_eight_rect_symboless, machine_code_five_rect)
        self.sequence_helper(test_string_five_max_symboless, machine_code_four_max)
        self.sequence_helper(test_string_six_pong_symboless, machine_code_five_pong)


class TestSymbolTranslator(unittest.TestCase):
    def test_symbol_translator_own(self):
        a = Assembler()
        self.assertEqual(a.symbol_translator(whitespace_result_string_one), symbol_translated_one)
        self.assertEqual(a.symbol_translator(whitespace_result_string_two), symbol_translated_two)


class TestAssembler(unittest.TestCase):
    def test_assembler(self):
        # self.maxDiff = None
        a = Assembler()
        # self.assertEqual(a.assemble_instructions(test_string_one), machine_code_one)
        # self.assertEqual(a.assemble_instructions(test_string_two), machine_code_two)
        # self.assertEqual(a.assemble_instructions(test_string_four_max), machine_code_four_max)
        self.assertEqual(a.assemble_instructions(test_string_nine_rect), machine_code_five_rect)
        self.assertEqual(a.assemble_instructions(test_string_seven_pong), machine_code_five_pong)
