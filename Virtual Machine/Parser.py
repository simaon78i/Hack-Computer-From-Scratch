"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """
    # Parser
    
    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient 
    access to their components. 
    In addition, it removes all white space and comments.

    ## VM Language Specification

    A .vm file is a stream of characters. If the file represents a
    valid program, it can be translated into a stream of valid assembly 
    commands. VM commands may be separated by an arbitrary number of whitespace
    characters and comments, which are ignored. Comments begin with "//" and
    last until the line's end.
    The different parts of each VM command may also be separated by an arbitrary
    number of non-newline whitespace characters.

    - Arithmetic commands:
      - add, sub, and, or, eq, gt, lt
      - neg, not, shiftleft, shiftright
    - Memory segment manipulation:
      - push <segment> <number>
      - pop <segment that is not constant> <number>
      - <segment> can be any of: argument, local, static, constant, this, that, 
                                 pointer, temp
    - Branching (only relevant for project 8):
      - label <label-name>
      - if-goto <label-name>
      - goto <label-name>
      - <label-name> can be any combination of non-whitespace characters.
    - Functions (only relevant for project 8):
      - call <function-name> <n-args>
      - function <function-name> <n-vars>
      - return
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Gets ready to parse the input file.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is to read all the lines of the input:
        self.input_lines = input_file.read().splitlines()
        self.current_command_index = -1
        self.current_line = ""

        #one value to a set of keys, for example, "add" is a key for "C_ARITHMETIC", "push" is a key for "C_PUSH" and so on.

        self.arithmetic_cmd_dict ={ 
            ("add","sub","neg","eq","gt","lt","and","or","not","shiftleft","shiftright")
            :"C_ARITHMETIC" }
        
        self.other_cmd_dict = {
            "push":"C_PUSH","pop":"C_POP","label":"C_LABEL","goto":"C_GOTO"
            ,"if-goto":"C_IF","function":"C_FUNCTION","call":"C_CALL","return":"C_RETURN"
        }

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        # Your code goes here!
        return self.current_command_index<len(self.input_lines)-1
        

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current 
        command. Should be called only if has_more_commands() is true. Initially
        there is no current command.
        """
        # Your code goes here!
        
        while self.current_command_index < len(self.input_lines)-1:
           self.current_command_index+=1
           self.current_line=self.input_lines[self.current_command_index].split("//")[0].strip()
           if self.current_line !="":
               return
            

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        # Your code goes here!
        first_word = self.current_line.split()[0]
        if first_word in self.other_cmd_dict:
            return self.other_cmd_dict[first_word]
        return next((self.arithmetic_cmd_dict[key] 
            for key in self.arithmetic_cmd_dict if first_word in key ),None)

    def arg1(self) -> str:
        """
        Returns:
            str: the first argument of the current command. In case of 
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned. 
            Should not be called if the current command is "C_RETURN".
        """
        # Your code goes here!
        split_line = self.current_line.split()
        if self.command_type() == "C_ARITHMETIC":
            return split_line[0]
        else:
            return split_line[1]

    def arg2(self) -> int:
        """
        Returns:
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP", 
            "C_FUNCTION" or "C_CALL".
        """
        # Your code goes here!
        return int(self.current_line.split()[2])
