# Hack Computer from Scratch: Hardware & Software Bridge

A bottom-up implementation of a modern 16-bit computer system, starting from fundamental NAND gates and progressing up to a functional assembler. This project demonstrates a deep understanding of computer architecture, digital logic, and the interface between hardware and software.

## 🏗️ System Architecture

The system is built in hierarchical layers, where each layer abstracts the complexity of the one beneath it.

### 1. The Hardware Layer (Digital Logic Design)
In this phase, I designed and implemented the entire chipset using Hardware Description Language (HDL).
*   **Elementary Logic:** Implementation of all basic gates (AND, OR, XOR, Mux) starting solely from a NAND gate.
*   **Arithmetic Logic Unit (ALU):** A 16-bit ALU capable of executing a variety of arithmetic and logical operations, forming the "brain" of the CPU.
*   **Memory Hierarchy (Sequential Logic):** Construction of 16-bit registers and RAM modules (up to 16K) using Flip-Flops, managing state and data persistence.
*   **Central Processing Unit (CPU):** Integration of the ALU, registers, and control logic to execute 16-bit instructions, manage memory access, and handle program flow.

### 2. The Low-Level Software Layer (Machine Language)
Before building the assembler, I explored the hardware's capabilities through direct machine-level programming.
*   **Instruction Set Architecture (ISA):** Mastery of the Hack binary format (A-instructions and C-instructions).
*   **Low-Level Programming:** Development of assembly programs that interact directly with memory-mapped I/O (Screen and Keyboard).

### 3. The Translation Layer (The Assembler)
The bridge between human-readable code and machine-executable binary.
*   **Symbolic Translation:** A software tool that parses assembly language and manages a symbol table for labels and variables.
*   **Binary Generation:** Automating the conversion of assembly mnemonics into 16-bit binary code ready to be loaded into the hardware's Instruction Memory (ROM).

---

## 📂 Repository Structure

The repository is organized by the logical progression of the system's construction:

*   **`Hardware-Logic/`** - Implementation of combinational and sequential chips (HDL).
*   **`Computer-Architecture/`** - The final CPU and Memory integration.
*   **`Assembler/`** - Source code for the symbolic-to-binary translator.
*   **`Assembly-Programs/`** - Low-level code samples demonstrating the computer in action.

---

## 🛠 Tech Stack

*   **Hardware Description:** HDL (Hardware Description Language)
*   **Software Implementation:** [Enter Language, e.g., C# / Python / Node.js]
*   **Simulation Tools:** Nand2Tetris Hardware Simulator & CPU Emulator

---

## 📜 Acknowledgments
This project is based on the "Nand2Tetris" curriculum (The Elements of Computing Systems) by Noam Nisan and Shimon Schocken.
