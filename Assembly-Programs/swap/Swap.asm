// This file is part of nand2tetris, as taught in The Hebrew University, and
// was written by Aviv Yaish. It is an extension to the specifications given
// [here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
// as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
// Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).

// The program should swap between the max. and min. elements of an array.
// Assumptions:
// - The array's start address is stored in R14, and R15 contains its length
// - Each array value x is between -16384 < x < 16384
// - The address in R14 is at least >= 2048
// - R14 + R15 <= 16383
//
// Requirements:
// - Changing R14, R15 is not allowed.

// Put your code here.
@i
M=1
@R14
A=M
D=M
@min
M=D
@R14
D=M
@min_add
M=D
@R14
A=M
D=M
@max
M=D
@R14
D=M
@max_add
M=D
(MIN_LOOP)
    @R15
    D=M
    @i
    D=D-M
    @MIN_STOP
    D;JEQ
        @R14
        D=M
        @i
        D=D+M
        @current
        M=D
        A=D
        D=M
        @min
        D=D-M
        @MIN_SKIP
        D;JGE
        @current
        A=M
        D=M
        @min
        M=D
        @current
        D=M
        @min_add
        M=D
        (MIN_SKIP)
        @i
        M=M+1
        @MIN_LOOP
        0;JMP
(MIN_STOP)
@i
M=1

(MAX_LOOP)
    @R15
    D=M
    @i
    D=D-M
    @MAX_STOP
    D;JEQ
        @R14
        D=M
        @i
        D=D+M
        @current
        M=D
        A=D
        D=M
        @max
        D=D-M
        @MAX_SKIP
        D;JLE
        @current
        A=M
        D=M
        @max
        M=D
        @current
        D=M
        @max_add
        M=D
        (MAX_SKIP)
        @i
        M=M+1
        @MAX_LOOP
        0;JMP
(MAX_STOP)
@min
D=M
@max_add
A=M
M=D
@max
D=M
@min_add
A=M
M=D


(END)
    @END
    0;JMP
