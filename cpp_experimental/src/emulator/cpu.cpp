#include <cassert>

#include "instr.hpp"
#include "cpu.hpp"

CPU::CPU(std::string id, std::vector<std::string> code) {
    this->id = id;

    for (auto line: code) {
        this->code.push_back(line);
    }
}

int64_t CPU::get_reg(int reg_index) {
    assert(reg_index >= 0);
    assert(reg_index < 32);

    return this->registers[reg_index];
}

int64_t CPU::get_mem(int mem_index) {
    assert(mem_index >= 0);
    assert(mem_index < MEMSIZE - 7);

    int64_t val = 0;
    for (int i = 0; i < 8; i++) {
        val <<= 8;
        val |= this->data_mem[mem_index + i];
    }

    return val;
}

void CPU::set_reg(int reg_index, int64_t val) {
    assert(reg_index >= 0);
    assert(reg_index < 32);

    this->registers[reg_index] = val;
}

void CPU::set_mem(int mem_index, int64_t val) {
    assert(mem_index >= 0);
    assert(mem_index < MEMSIZE - 7);

    for (int i = 7; i >= 0; i--) {
        uint8_t cur = val & 0xFF;
        val >>= 8;
        this->data_mem[mem_index + i] = cur;
    }
}


std::string _formatted_hex(int64_t num) {
    std::stringstream ss;
    ss << std::hex << std::uppercase << std::setw(16) << std::setfill('0') << num;
    std::string hex_str = ss.str();

    std::string formattedString;
    for (std::size_t i = 0; i < hex_str.length(); i += 2) {
        if (i > 0) { formattedString += ' '; }
        formattedString += hex_str.substr(i, 2);
    }

    return formattedString;
}

void CPU::print_hex() {
    int prefix_len = ("CPU ID: " + this->id + " ").size();
    std::cout 
        << "CPU ID: " << this->id << " " 
        << std::setw(76 - prefix_len) << std::setfill('-') << ""
        << std::endl << std::endl;

    std::cout << "PC = " << this->pc << std::endl;

    std::cout << std::endl << "Registers:" << std::endl;
    for (int i = 0; i < 16; i++) {
        std::cout << "\t";
        if (i <= 9) { std::cout << " "; }
        std::cout 
            << "X" << i << ": " << _formatted_hex(this->registers[i])
            << "\t||\t"
            << "X" << (i + 16) << ": " << _formatted_hex(this->registers[i + 16])
            << std::endl;
    }

    std::cout << std::endl << "Data Memory:" << std::endl;
    for (int i = 0; i < (MEMSIZE / 2); i += 8) {
        int64_t num1 = this->get_mem(i);
        int64_t num2 = this->get_mem(MEMSIZE / 2 + i);

        std::cout << "\t";

        if (i <= 9) { std::cout << "  "; }
        else if (i <= 99) { std::cout << " "; }

        std::cout 
            << i << ": " << _formatted_hex(num1)
            << "\t||\t"
            << (MEMSIZE / 2 + i) << ": " << _formatted_hex(num2)
            << std::endl;
    }

    std::cout << std::endl << std::setw(76) << std::setfill('-') << "" << std::endl;

}

void CPU::print_dec() {
    
}