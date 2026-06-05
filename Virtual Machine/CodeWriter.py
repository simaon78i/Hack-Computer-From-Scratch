"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from textwrap import dedent

class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.output_stream = output_stream
        self.lable_counter = 0
        self.filename=""
        self.function_name = []

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment. For example, in order to prevent collisions between two
        # .vm files which push/pop to the static segment, one can use the current
        # file's name in the assembly variable's name and thus differentiate between
        # static variables belonging to different files.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        # For example, using code similar to:
        # input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
        self.filename = filename

    def write_init(self) -> None:
        init_asm = dedent("""
            @256
            D=A
            @SP
            M=D
            @256
            D=A
            @LCL
            M=D
            @256
            D=A
            @ARG
            M=D
        """)
        self.output_stream.write(init_asm + "\n")
        self.write_call("Sys.init", 0)

    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given 
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        # Your code goes here!
        if command == "add":
            self.arithmetic_add()
        elif command =="sub":
            self.arithmetic_sub()
        elif command=="and":
            self.arithmetic_and()
        elif command =="or":
            self.arithmetic_or()
        elif command =="neg":
            self.arithmetic_neg()
        elif command == "not":
            self.arithmetic_not()
        elif command in ["eq","gt","lt"]:
            self.arithmetic_jump(command)

    def arithmetic_jump(self, command):
        jump_cmd = "JEQ" if command=="eq" else( "JGT" if command =="gt" else "JLT")
        assembly_command = dedent(f"""\
                                @SP
                                M=M-1
                                A=M
                                D=M
                                @SP
                                A=M-1
                                D=M-D
                                @IF_TRUE_{self.lable_counter}
                                D;{jump_cmd}
                                @SP
                                A=M-1
                                M=0
                                @IF_FALSE_{self.lable_counter}
                                0;JMP
                                (IF_TRUE_{self.lable_counter})
                                @SP
                                A=M-1
                                M=-1
                                (IF_FALSE_{self.lable_counter})
                                """)
        self.output_stream.write(assembly_command+"\n")
        self.lable_counter+=1

    def arithmetic_not(self):
        assembly_command=dedent("""\
                                @SP
                                A=M-1
                                M=!M
                                """)
        self.output_stream.write(assembly_command +"\n")

    def arithmetic_neg(self):
        assembly_command=dedent("""\
                                @SP
                                A=M-1
                                M=-M
                                """)
        self.output_stream.write(assembly_command +"\n")

    def arithmetic_or(self):
        assembly_command=dedent("""\
                                    @SP
                                    M=M-1
                                    A=M
                                    D=M
                                    @SP
                                    A=M-1
                                    M=M|D            
                                    """)
        self.output_stream.write(assembly_command +"\n")

    def arithmetic_and(self):
        assembly_command=dedent("""\
                            @SP
                            M=M-1
                            A=M
                            D=M
                            @SP
                            A=M-1
                            M=M&D            
                            """)
        self.output_stream.write(assembly_command +"\n")

    def arithmetic_sub(self):
        assembly_command=dedent("""\
                                @SP
                                M=M-1
                                A=M
                                D=M
                                @SP
                                A=M-1
                                M=M-D
                                """)
        self.output_stream.write(assembly_command +"\n")

    def arithmetic_add(self):
        assembly_command = dedent("""\
                                @SP
                                M=M-1
                                A=M
                                D=M
                                @SP
                                A=M-1
                                M=M+D 
                            """)
        self.output_stream.write(assembly_command +"\n")

        
    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.
        if command == "C_PUSH":
            self.push(segment, index)
        elif command == "C_POP":
            self.pop(segment, index)

    def pop(self, segment, index):
        if segment in ["local", "argument", "this", "that"]:
            self.pop_others(segment, index)
        elif segment == "temp":
            self.pop_temp(index)

        elif segment == "pointer":
            self.pop_pointer(index)

        elif segment == "static":
            self.pop_static(index)

    def pop_static(self, index):
        assembly_cmd = dedent(f"""\
                        @SP
                        M=M-1
                        A=M
                        D=M
                        @{self.filename}.{index}
                        M=D
                        """)
        self.output_stream.write(assembly_cmd+"\n")

    def pop_pointer(self, index):
        address = 3 if index == 0 else 4
        assembly_cmd = dedent(f"""\
                            @SP
                            M=M-1
                            A=M
                            D=M
                            @{address}
                            M=D
                            """)
        self.output_stream.write(assembly_cmd+"\n")

    def pop_temp(self, index):
        assembly_cmd = dedent(f"""\
                        @SP
                        M=M-1
                        A=M
                        D=M
                        @{index + 5}
                        M=D
                        """)
        self.output_stream.write(assembly_cmd+"\n")

    def pop_others(self, segment, index):
        base_idx = "LCL" if segment == "local" else (
                    "ARG" if segment == "argument" else (
                        "THIS" if segment == "this" else "THAT")
                )
        assembly_cmd = dedent(f"""\
                        @{index}
                        D=A
                        @{base_idx}
                        D=D+M
                        @R13
                        M=D
                        @SP
                        M=M-1
                        A=M
                        D=M
                        @R13
                        A=M
                        M=D
                        """)
        self.output_stream.write(assembly_cmd+"\n")

    def push(self, segment, index):
        if segment == "constant":
            self.push_constant(index)
        elif segment in ["local", "argument", "this", "that"]:
            self.push_others(segment, index)
        elif segment=="temp":
            self.push_temp(index)
        elif segment == "pointer":
            self.push_pointer(index)
        elif segment == "static":
            self.push_static(index)

    def push_static(self, index):
        assembly_cmd = dedent(f"""\
                    @{self.filename}.{index}
                    D=M
                    @SP
                    A=M
                    M=D
                    @SP
                    M=M+1
                    """)
        self.output_stream.write(assembly_cmd+"\n")

    def push_pointer(self, index):
        address = 3 if index ==0 else 4
        assembly_cmd = dedent(f"""\
                        @{address}
                        D=M
                        @SP
                        A=M
                        M=D
                        @SP
                        M=M+1
                        """)
        self.output_stream.write(assembly_cmd+"\n")

    def push_temp(self, index):
        assembly_cmd = dedent(f"""\
                        @{index+5}
                        D=M
                        @SP
                        A=M
                        M=D
                        @SP
                        M=M+1
                        """)
        self.output_stream.write(assembly_cmd+"\n")

    def push_others(self, segment, index):
        base_idx = "LCL" if segment == "local" else (
                    "ARG" if segment == "argument" else (
                        "THIS" if segment == "this" else "THAT")
                )
        assembly_cmd = dedent(f"""\
                            @{index}
                            D=A
                            @{base_idx}
                            D=M+D
                            A=D
                            D=M
                            @SP
                            A=M
                            M=D
                            @SP
                            M=M+1
                            """)
        self.output_stream.write(assembly_cmd+"\n")

    def push_constant(self, index):
        assembly_cmd = dedent(f"""\
                                @{index}
                                D=A
                                @SP
                                A=M
                                M=D
                                @SP
                                M=M+1
                                """)
        self.output_stream.write(assembly_cmd+"\n")

    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command. 
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        if not self.function_name:
            full_label = label
        else:
            full_label = f"{self.function_name[-1]}${label}"
        assembly_cmd = dedent(f"""
                                ({full_label})
                                 """)
        self.output_stream.write(assembly_cmd+"\n")
                              
    
    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        if not self.function_name:
            full_label = label
        else:
                full_label = f"{self.function_name[-1]}${label}"
        assembly_cmd = dedent(f"""
                                @{full_label}
                                0;JMP
                                """)
        self.output_stream.write(assembly_cmd+"\n")
    
    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command. 

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        if not self.function_name:
            full_label = label
        else:
            full_label = f"{self.function_name[-1]}${label}"
        assembly_cmd = dedent(f"""
                                @SP
                                M=M-1
                                A=M
                                D=M
                                @{full_label}
                                D;JNE
                                """)
        self.output_stream.write(assembly_cmd+"\n")
    
    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command. 
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this 
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0
        self.function_name.append(function_name)
        assembly_cmd = dedent(f"""
                                ({function_name})
                                """)
        self.output_stream.write(assembly_cmd+"\n")
        for _ in range(n_vars):
            self.push_constant(0)
    
    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command. 
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's 
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        # ARG = SP-5-n_args     // repositions ARG
        # LCL = SP              // repositions LCL
        # goto function_name    // transfers control to the callee
        # (return_address)      // injects the return address label into the code
        if not self.function_name:
            caller_name = "Bootstrap"  
        else:
            caller_name = self.function_name[-1]
        assembly_cmd = dedent(f"""
                            @{caller_name}$ret.{self.lable_counter}
                            D=A
                            @SP
                            A=M
                            M=D
                            @SP
                            M=M+1
                            @LCL
                            D=M
                            @SP
                            A=M
                            M=D
                            @SP
                            M=M+1
                            @ARG
                            D=M
                            @SP
                            A=M
                            M=D
                            @SP
                            M=M+1
                            @THIS
                            D=M
                            @SP
                            A=M
                            M=D
                            @SP
                            M=M+1
                            @THAT
                            D=M
                            @SP
                            A=M
                            M=D
                            @SP
                            M=M+1
                            @SP
                            D=M
                            @{n_args}
                            D=D-A
                            @5
                            D=D-A
                            @ARG
                            M=D
                            @SP
                            A=M
                            D=A
                            @LCL
                            M=D
                            @{function_name}
                            0;JMP
                            ({caller_name}$ret.{self.lable_counter})
                            """)
        self.output_stream.write(assembly_cmd+"\n")
        self.lable_counter+=1

        
    
    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        # return_address = *(frame-5)   // puts the return address in a temp var
        # *ARG = pop()                  // repositions the return value for the caller
        # SP = ARG + 1                  // repositions SP for the caller
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        # goto return_address           // go to the return address
        assembly_cmd = dedent(f"""
                            @LCL
                            D=M
                            @R13
                            M=D
                            
                            @R13
                            D=M
                            @5
                            A=D-A
                            D=M
                            @R14
                            M=D
                            
                            @SP
                            M=M-1
                            A=M
                            D=M
                            @ARG
                            A=M
                            M=D
                            
                            @ARG
                            D=M+1
                            @SP
                            M=D
                            
                            @R13
                            D=M
                            @1
                            A=D-A
                            D=M
                            @THAT
                            M=D
                            
                            @R13
                            D=M
                            @2
                            A=D-A
                            D=M
                            @THIS
                            M=D
                            
                            @R13
                            D=M
                            @3
                            A=D-A
                            D=M
                            @ARG
                            M=D
                            
                            @R13
                            D=M
                            @4
                            A=D-A
                            D=M
                            @LCL
                            M=D
                              
                            @R14
                            A=M
                            0;JMP
                            """)
        self.output_stream.write(assembly_cmd+"\n")
