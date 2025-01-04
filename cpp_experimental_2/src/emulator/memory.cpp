#include "memory.hpp"

Memory::Memory(std::vector<uint32_t> code) {
    /*
        - code is a list of words
        - if the last word of the code fit's into memory, access is valid
        - byte_index of the last word of the code = ((code.size() - 1) * 4)
    */
    this->validate_access(
        ((code.size() - 1) * (int)AccessLength::WORD), 
        AccessLength::WORD
    );

    // Copy the code into main memory
    std::memcpy(this->memory, code.data(), (code.size() * sizeof(uint32_t)));
}

void Memory::validate_access(uint byte_index, AccessLength length) {
    if ((byte_index < 0) || (byte_index + (int)length > MEM_SIZE)) {
        // Throw Exception
        perror("Error in Memory Access.");
    }
}

uint8_t Memory::get_byte(uint byte_index) {
    this->validate_access(byte_index, AccessLength::BYTE);
    
    uint8_t data;
    // Reading data from main-memory
    std::memcpy(&data, (this->memory + byte_index), sizeof(uint8_t));

    return data;
}

void Memory::set_byte(uint byte_index, uint8_t val) {
    this->validate_access(byte_index, AccessLength::BYTE);

    // Copying val to main-memory
    std::memcpy((this->memory + byte_index), &val, sizeof(uint8_t));
}

uint32_t Memory::get_word(uint byte_index) {
    this->validate_access(byte_index, AccessLength::WORD);
    
    uint32_t data;
    // Reading data from main-memory
    std::memcpy(&data, (this->memory + byte_index), sizeof(uint32_t));
    
    return data;
}

void Memory::set_word(uint byte_index, uint32_t val) {
    this->validate_access(byte_index, AccessLength::WORD);

    // Copying val to main-memory
    std::memcpy((this->memory + byte_index), &val, sizeof(uint32_t));
}

uint64_t Memory::get_double_word(uint byte_index) {
    this->validate_access(byte_index, AccessLength::DOUBLE_WORD);

    uint64_t data;
    // Reading data from main-memory
    std::memcpy(&data, (this->memory + byte_index), sizeof(uint64_t));
    
    return data;
}

void Memory::set_double_word(uint byte_index, uint64_t val) {
    this->validate_access(byte_index, AccessLength::DOUBLE_WORD);
    
    // Copying val to main-memory
    std::memcpy((this->memory + byte_index),&val, sizeof(uint64_t));
}

void Memory::randomize() {
    /*
        - '/dev/urandom' generates random data
        - reading 'MEM_SIZE' bytes from this file into 
            the emulator's main-memory
        - Should work on Linux and MacOS
    */
    std::ifstream urandom("/dev/urandom", std::ios::binary);
    if (!urandom.read(reinterpret_cast<char*>(this->memory), MEM_SIZE)) {
        perror("Error in Randomizing Memory.");  // Throw Exception
    }
}