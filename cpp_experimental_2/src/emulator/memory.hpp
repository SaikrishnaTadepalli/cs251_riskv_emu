#ifndef MEMORY_HPP
#define MEMORY_HPP

#include <iostream>
#include <vector>
#include <random>
#include <sys/random.h>
#include <unistd.h>
#include <fstream>
#include <stdexcept>

// in Bytes
#define MEM_SIZE 1024

class Memory {
public:
    uint8_t memory[MEM_SIZE] = { 0 };
    enum AccessLength { BYTE = 1, WORD = 4, DOUBLE_WORD = 8};

    Memory(std::vector<uint32_t> code);

    void validate_access(uint byte_index, AccessLength length);

    uint8_t get_byte(uint byte_index);
    void set_byte(uint byte_index, uint8_t val);

    uint32_t get_word(uint word_index);
    void set_word(uint word_index, uint32_t val);

    uint64_t get_double_word(uint double_word_index);
    void set_double_word(uint double_word_index, uint64_t val);

    void randomize();
};

#endif