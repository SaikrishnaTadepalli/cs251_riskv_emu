#include "instr.hpp"
#include "cpu.hpp"

CPU::CPU(std::string id, std::vector<std::string> code) {
    this->id = id;
    this-> pc = 0;

    for (auto line: code) {
        this->code.push_back(line);
    }

    this->randomize_cpu();
}

int64_t CPU::get_reg(int reg_index) const {
    assert(reg_index >= 0);
    assert(reg_index < 32);

    return this->registers[reg_index];
}

int64_t CPU::get_mem(int mem_index) const {
    assert(mem_index >= 0);
    assert(mem_index < MEMSIZE - 7);
    assert(mem_index % 8 == 0);

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
    assert(mem_index % 8 == 0);

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

std::string _formatted_dec (int64_t num) {
    std::string s = std::to_string(num);
    while (s.length() < 20) { s = " " + s; }
    return s;
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

    std::cout << std::endl << std::setw(76) << std::setfill('-') << "" << std::endl << std::endl;

}

void CPU::print_dec() {
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
            << "X" << i << ": " << _formatted_dec(this->registers[i])
            << "\t||\t"
            << "X" << (i + 16) << ": " << _formatted_dec(this->registers[i + 16])
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
            << i << ": " << _formatted_dec(num1)
            << "\t||\t"
            << (MEMSIZE / 2 + i) << ": " << _formatted_dec(num2)
            << std::endl;
    }

    std::cout << std::endl << std::setw(76) << std::setfill('-') << "" << std::endl << std::endl;
}

void CPU::set_print_mode(CPU::PrintMode new_mode) {
    this->print_mode = new_mode;
}

void CPU::print() {
    if (this->print_mode == CPU::PrintMode::DEC) { this->print_dec();} 
    else { this->print_hex(); }
}

bool _reg_eq(const CPU &cpu1, const CPU &cpu2) {
    for (int i = 0; i < 32; i++) {
        if (cpu1.get_reg(i) != cpu2.get_reg(i)) { return false; }
    }
    return true;
}

bool _mem_eq(const CPU &cpu1, const CPU &cpu2) {
    for (int i = 0; i < MEMSIZE; i+=8) {
        if (cpu1.get_mem(i) != cpu2.get_mem(i)) { return false; }
    }
    return true;
}

bool CPU::operator==(const CPU& other) const {    
    return _reg_eq(*this, other) && _mem_eq(*this, other);
}

bool CPU::operator!=(const CPU& other) const {
    return !(*this == other);
}

void CPU::randomize_registers() {
    std::random_device rd;
    std::mt19937_64 gen(rd());

    for (int i = 0; i < 31; i++) {
        std::uniform_int_distribution<int64_t> dist;
        int64_t val = dist(gen);
        this->set_reg(i, val);
    }
}

void CPU::randomize_dmem() {
    std::random_device rd;
    std::mt19937_64 gen(rd());

    for (int i = 0; i < MEMSIZE; i+=8) {
        std::uniform_int_distribution<int64_t> dist;
        int64_t val = dist(gen);
        this->set_mem(i, val);
    }
}

void CPU::randomize_cpu() {
    this->randomize_registers();
    this->randomize_dmem();
}

Instr CPU::get_cur_instr() {
    int i = (this->pc / 4);
    assert(i < int(this->code.size()));

    Instr instr = Instr(this->code[i]);
    return instr;
}

void CPU::run_instr() {
    Instr cur_instr = this->get_cur_instr();

    switch (cur_instr.type) {
        case Instr::InstructionType::R: {
            int XA = cur_instr.args[0];
            int XB = cur_instr.args[1];
            int XC = cur_instr.args[2];

            int64_t new_val = 0;
            if (cur_instr.instr == Instr::Instruction::ADD) {
                new_val = this->registers[XB] + this->registers[XC];
            } else {
                new_val = this->registers[XB] - this->registers[XC];
            }

            this->registers[XA] = new_val;
            this->pc += 4;

            break;
        } case Instr::InstructionType::D: {
            int XA = cur_instr.args[0];
            int XB = cur_instr.args[1];
            int IMM = cur_instr.args[2];

            int mem_index = this->registers[XB] + IMM;
            if (cur_instr.instr == Instr::Instruction::LDUR) {
                int64_t mem_value = this->get_mem(mem_index);
                this->registers[XA] = mem_value;
            } else {
                int64_t reg_val = this->registers[XA];
                this->set_mem(mem_index, reg_val);
            }

            this->pc += 4;
            break;
        } case Instr::InstructionType::I: {
            int XA = cur_instr.args[0];
            int XB = cur_instr.args[1];
            int IMM = cur_instr.args[2];

            int64_t new_val = 0;
            if (cur_instr.instr == Instr::Instruction::ADDI) {
                new_val = this->registers[XB] + (int64_t)IMM;
            } else {
                new_val = this->registers[XB] - (int64_t)IMM;
            }

            this->registers[XA] = new_val;
            this->pc += 4;
            break;
        } case Instr::InstructionType::B: {
            int IMM = cur_instr.args[0];

            this->pc += 4 * IMM;
            break;
        } case Instr::InstructionType::CB: {
            int XA = cur_instr.args[0];
            int IMM = cur_instr.args[1];

            int step = 1;
            if (cur_instr.instr == Instr::Instruction::CBZ) {
                if (this->registers[XA] == 0) {
                    step = IMM;
                }
            } else {
                if (this->registers[XA] != 0) {
                    step = IMM;
                }
            }

            this->pc += 4 * step;
            break;
        }
    }
}

void CPU::run() {
    while (this->pc < uint32_t(this->code.size()) * 4) {
        this->run_instr();
    }
}

void CPU::step() {
    std::cout << "Executing " << std::setw(66) << std::setfill('=') << "" << std::endl << std::endl;
    std::cout << "Initial State: " << std::endl << std::endl;

    this->print();
    while (this->pc < uint32_t(this->code.size()) * 4) {
        std::cout << "('enter' to continue)" << std::endl;
        std::cin.get();

        int cur_instr_index = (this->pc / 4);
        for (int i = 0; i < int(this->code.size()); i++) {
            std::string line = this->code[i];

            while (line.size() < size_t(20)) { 
                line += " "; 
            }

            if (i == cur_instr_index) {
                line += "\t<<< Just Executed";
            }

            std::cout << line << std::endl;
        }
        
        std::cout << std::endl;

        this->run_instr();
        this->print();
    }

    std::cout << "Finished " << std::setw(67) << std::setfill('=') << "" << std::endl << std::endl;
}
