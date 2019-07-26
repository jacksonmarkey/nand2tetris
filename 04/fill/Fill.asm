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

// checks whether there is keyboard input
(CHECK1)
@24576
D=M
@CHECK1
D;JEQ

// colors every pixel black
@i // index register for looping
M=0
(LOOP1)
@8192
D=A
@i
D=M-D
@CHECK2
D;JGE // jumps out of loop if index loop M-value is nonnegative, i.e. if the loop
      // has been carried out 8912 times
@16384
D=A
@i
A=D+M
M=-1 // colors the M-th pixel black
@i
M=M+1
@LOOP1
0;JMP // return to the top of the loop after incrementing

// checks whether there is no keyboard input
(CHECK2)
@24576
D=M
@CHECK2
D;JNE

// colors every pixel white
@i // index register
M=0
(LOOP2)
@8192
D=A
@i
D=M-D
@CHECK1
D;JGT // goes back to the first loop in the chip if we've already set all the
      // pixels to white, i.e. if we've iterated through all 8912 pixels
@16384
D=A
@i
A=D+M
M=0 // writes the M-th pixel black
@i
M=M+1
@LOOP2
0;JMP // repeats this loop after incrementing
