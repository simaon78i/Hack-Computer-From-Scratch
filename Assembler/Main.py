"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code


def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # A good place to start is to initialize a new Parser object:
    # parser = Parser(input_file)
    # Note that you can write to output_file like so:
    # output_file.write("Hello world! \n")

    table= SymbolTable()
    code= Code()
    
    lines_counter=0
    current_address=16

    tags_parser = Parser(input_file)
    add_tags(tags_parser, table, lines_counter)

    input_file.seek(0)
    vars_parser = Parser(input_file)
    add_vars(vars_parser, table, current_address)

    input_file.seek(0)
    write_parser = Parser(input_file)
    write_output(write_parser, table, code, output_file)


def add_tags(parser : Parser, table : SymbolTable, lines_counter: int)->None:
    #print("add_tags.....")
    while parser.has_more_commands():
        if parser.command_type() == "L_COMMAND":
            new_symbole=parser.symbol()
            table.add_entry(new_symbole,lines_counter)
        elif parser.command_type()=="A_COMMAND" or parser.command_type()=="C_COMMAND":
            lines_counter+=1
        parser.advance()

def add_vars(parser : Parser, table : SymbolTable, current_address : int)->None:
    #print("add_vars.....")
    while parser.has_more_commands():
        if parser.command_type()=="A_COMMAND":
            new_symbole=parser.symbol()
            if (not new_symbole.isdigit()) and (not table.contains(new_symbole)):
                print(f"Adding new variable: {new_symbole} with address: {current_address}")
                table.add_entry(new_symbole,current_address)
                current_address+=1
        parser.advance()


def write_output(parser : Parser, table : SymbolTable, code : Code, output_file : typing.TextIO)-> None:
    #print("write_output.....")
    while parser.has_more_commands():
        if parser.command_type() == "A_COMMAND":
            symbole=parser.symbol()
            if symbole.isdigit():
                address=int(symbole)
            else:
                address=table.get_address(symbole)
            binary_line = "0" + f"{int(address):015b}"
            output_file.write(binary_line+"\n")

        elif parser.command_type() == "C_COMMAND":
            ones = "111"
            dest = code.dest(parser.dest())
            comp = code.comp(parser.comp())
            jump = code.jump(parser.jump())
            
            output_file.write(ones+comp+dest+jump+"\n")
        parser.advance()



if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
