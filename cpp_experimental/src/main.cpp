#include <iostream>
#include <vector>
#include <string>
#include <fstream>

#include "emulator/instr.hpp"
#include "emulator/cpu.hpp"

std::vector<std::string> read_file(const std::string &filename) {
    std::ifstream file(filename);
    
    std::vector<std::string> lines;
    if (!file.is_open()) {
        std::cerr << "Unable to open file: " << filename << std::endl;
        return lines;
    }
    
    std::string line;
    while (std::getline(file, line)) {
        lines.push_back(line);
    }

    file.close();

    return lines;
}

int main() {
    std::vector<std::string> code1 = read_file("../programs/prog1.asm");

    CPU cpu1 = CPU("cpu1", code1);
    cpu1.step();

    return 0;
}

























