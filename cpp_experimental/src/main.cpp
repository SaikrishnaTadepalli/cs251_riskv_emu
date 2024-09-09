#include <iostream>
#include <string.h>

#include "emulator/instr.hpp"
#include "emulator/cpu.hpp"

int main() {
    std::vector<std::string> lines;

    lines.push_back("ADDI X3, XZR, #20");
    lines.push_back("ADD X4, X3, X3");
    lines.push_back("SUBI X5, X4, #12");

    CPU cpu1 = CPU("cpu1", lines);
    cpu1.step();
    // cpu1.print_hex();

    // cpu1.run_instr();
    // cpu1.print_hex();

    // cpu1.run_instr();
    // cpu1.print_hex();

    // cpu1.run_instr();
    // cpu1.print_hex();

    return 0;
}

























