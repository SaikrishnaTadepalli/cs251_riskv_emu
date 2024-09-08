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

    CPU cpu1 = CPU("cpu1", lines);

    cpu1.print_hex();

    cpu1.set_reg(0, 0x124df34acefd125);
    cpu1.set_reg(1, 0x124df34acefd1252);
    cpu1.set_reg(10, 0x124dfefd125);
    cpu1.set_reg(11, 0x12425);
    cpu1.set_reg(21, 0x5);
    cpu1.set_reg(25, 0x124df34acefd125);
    cpu1.set_reg(30, 0x124df345);
    cpu1.set_reg(31, 0xfff);
    cpu1.set_reg(1, 0xffffff);
    cpu1.set_reg(4, -32);
    cpu1.set_reg(5, 0x0);

    cpu1.set_mem(0, 0x124df34acefd125);
    cpu1.set_mem(8, 0x124df34acefd1252);
    cpu1.set_mem(32, 0x124dfefd125);
    cpu1.set_mem(72, 0x12425);
    cpu1.set_mem(120, 0x5);
    cpu1.set_mem(176, 0x124df34acefd125);
    cpu1.set_mem(216, 0x124df345);
    cpu1.set_mem(248, 0xfff);
    cpu1.set_mem(248, -32);

    cpu1.print_hex();

    std::cout<< "\n\n" << (cpu1 == cpu1) << "\n\n";

    std::cout << "\n^^^=======================================^^^\n" << std::endl;
    return 0;
}

























