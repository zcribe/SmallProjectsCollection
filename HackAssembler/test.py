import unittest

from .main import Assembler
from .sample_strings import test_string_one, test_string_two, whitespace_result_string_one, \
    whitespace_result_string_two, symbol_translated_one, symbol_translated_two


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


class TestSymbolTranslator(unittest.TestCase):
    def test_symbol_translator(self):
        a = Assembler()
        self.assertEqual(a.symbol_translator(whitespace_result_string_one), symbol_translated_one)
        self.assertEqual(a.symbol_translator(whitespace_result_string_two), symbol_translated_two)


class TestAssembler(unittest.TestCase):
    pass
