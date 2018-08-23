test_string_one = '''
// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(INIT)
    @SCREEN // Screen address alias
        D=A
    @PIXEL
        M=D

(MAINLOOP)
    @KBD // Keyboard address alias
        D=M

    @BLACK
        D;JNE
    @WHITE // Default
        0;JMP

(BLACK)
    @PIXEL // Pixel addition
        D=M
        M=M+1
        A=D
        M=-1
    @KBD // Last screenmap bit
        D=A-D
    @INIT // Reset
        D;JEQ
    @MAINLOOP
        0;JMP


(WHITE)
    @PIXEL
        D=M
        M=M+1
        A=D
        M=0
    @KBD
        D=A-D
    @INIT
        D;JEQ
    @MAINLOOP
        0;JMP
'''

test_string_two = '''// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

@R2
M=0
@R1
D=M
@counter
M=D

(Loop)
@R1 // Neg, Pos kontroll
D=M
@Negative
D;JLT
@Endless
D;JEQ


@R0 // Liitmis Loop
D=M
@R2
M=M+D
@counter
M=M-1
D=M
@Loop // Loop jump kui pole 0
D;JGT
@Endless
D;JEQ

(Negative)
@R0 // Lahutamise Loop
D=M
@R2
M=M-D
@counter
M=M+1
D=M
@Loop // Loop jump kui pole 0
D;JLT
@Endless
D;JEQ


@Endless
(Endless)
0;JMP'''

whitespace_result_string_one = '''(INIT)
@SCREEN
D=A
@PIXEL
M=D
(MAINLOOP)
@KBD
D=M
@BLACK
D;JNE
@WHITE
0;JMP
(BLACK)
@PIXEL
D=M
M=M+1
A=D
M=-1
@KBD
D=A-D
@INIT
D;JEQ
@MAINLOOP
0;JMP
(WHITE)
@PIXEL
D=M
M=M+1
A=D
M=0
@KBD
D=A-D
@INIT
D;JEQ
@MAINLOOP
0;JMP'''

whitespace_result_string_two = '''@R2
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
0;JMP'''

symbol_translated_one = '''@16384
D=A
@16
M=D
@24576
D=M
@12
D;JNE
@24
0;JMP
@16
D=M
M=M+1
A=D
M=-1
@24576
D=A-D
@0
D;JEQ
@5
0;JMP
@16
D=M
M=M+1
A=D
M=0
@24576
D=A-D
@0
D;JEQ
@5
0;JMP'''

symbol_translated_two = '''@16
M=0
@16
D=M
@17
M=D
@16
D=M
@24
D;JLT
@37
D;JEQ
@16
D=M
@16
M=M+D
@17
M=M-1
D=M
@6
D;JGT
@37
D;JEQ
@16
D=M
@16
M=M-D
@17
M=M+1
D=M
@6
D;JLT
@37
D;JEQ
@37
0;JMP'''
