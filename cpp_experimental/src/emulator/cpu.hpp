#ifndef CPU_HPP
#define CPU_HPP

#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <unordered_map>
#include <iomanip>
#include <bitset>

#define MEMSIZE 256

class CPU {
public:
    std::string id;
    std::vector<std::string> code;
    uint32_t pc;
    int64_t registers[32] = { 0 };
    uint8_t data_mem[MEMSIZE] = { 0 };

    CPU(std::string id, std::vector<std::string> code);

    int64_t get_reg(int reg_index);
    int64_t get_mem(int mem_index);

    void set_reg(int reg_index, int64_t val);
    void set_mem(int mem_index, int64_t val);

    void print_hex();
    void print_dec();
};

#endif