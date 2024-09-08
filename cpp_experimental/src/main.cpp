#include <iostream>
#include <string.h>

#include "emulator/instr.hpp"
#include "emulator/cpu.hpp"

const char *instrs_raw[] = {
    "ADD X1, X2, X3",
    "SUB X1, XZR, XZR",
    "LDUR X1, [X2, #24]",
    "STUR XZR, [XZR, #24]",
    "ADDI X0, X31, #0",
    "SUBI X3, X13, #12345",
    "B #-1245",
    "CBZ XZR #-124",
    "CBNZ X22 #0",
};

int main() {
    std::cout << "\n=============================================\n" << std::endl;

    // for (auto s: instrs_raw) {
    //     Instr instr = Instr(s);
    
    //     instr.print_verbose();
    // }

    std::vector<std::string> lines;
    lines.push_back("ADD X1, X2, X3");
    lines.push_back("SUB X1, XZR, XZR");
    lines.push_back("ADDI X0, X31, #0");

    CPU cppu1 = CPU("cpu1", lines);

    cppu1.print_hex();

    std::cout << "\n^^^=======================================^^^\n" << std::endl;
    return 0;
}

























