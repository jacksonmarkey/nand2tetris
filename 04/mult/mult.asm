// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

@i
M=0
@sum
M=0

(LOOP)

@0
D=M
@i
D=M-D
@RETURN // jumps out of the loop if we've already added R1 to itself R0 times
D;JGE
@i
M=M+1
@1
D=M
@sum
M=D+M
@LOOP
0;JMP

(RETURN)

@sum
D=M
@2
M=D

(END)

@END // end the program with an infinite loop
0;JMP
