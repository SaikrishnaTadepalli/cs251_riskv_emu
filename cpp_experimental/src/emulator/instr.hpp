#ifndef INSTR_HPP
#define INSTR_HPP

#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <stdexcept>

class Instr {
public:
    enum class InstructionType { 
        R, D, I, B, CB 
    };

    enum class Instruction { 
        ADD, SUB, LDUR, STUR, ADDI, SUBI, B, CBZ, CBNZ 
    };

    static const std::unordered_map<std::string, Instruction> InstructionMap;

    Instruction instr;
    InstructionType type;
    std::vector<int> args;

    Instr(std::string instr);

    static InstructionType get_instr_type(Instruction instruction);    

    void print_verbose();
};

#endif
