#include "instr.hpp"

// Define static member variable
const std::unordered_map<std::string, Instr::Instruction> Instr::InstructionMap = {
    {"ADD", Instr::Instruction::ADD},
    {"SUB", Instr::Instruction::SUB},
    {"LDUR", Instr::Instruction::LDUR},
    {"STUR", Instr::Instruction::STUR},
    {"ADDI", Instr::Instruction::ADDI},
    {"SUBI", Instr::Instruction::SUBI},
    {"B", Instr::Instruction::B},
    {"CBZ", Instr::Instruction::CBZ},
    {"CBNZ", Instr::Instruction::CBNZ}
};

// Constructor definition
Instr::Instr(std::string instr) {
    std::replace(instr.begin(), instr.end(), ',', ' ');
    std::replace(instr.begin(), instr.end(), '[', ' ');
    std::replace(instr.begin(), instr.end(), ']', ' ');
    std::replace(instr.begin(), instr.end(), '#', ' ');
    std::replace(instr.begin(), instr.end(), 'X', ' ');

    std::istringstream iss(instr);

    std::string token;
    iss >> token;

    try {
        this->instr = Instr::InstructionMap.at(token);
    } catch(std::out_of_range&) {
        std::string err_msg = "Instruction Unknown. Received '" + token + "'.";
        std::cerr << err_msg;
        exit(1);
    }
    
    this->type = Instr::get_instr_type(this->instr);

    while (iss >> token) {
        if (token == "ZR") {
            this->args.push_back(31);
        } else if (token == " " or token == "") {
            std::cerr << "SOMETHING WRONG" << std::endl;
        } else {
            this->args.push_back(std::stoi(token));
        }
    }
}


Instr::InstructionType Instr::get_instr_type(Instr::Instruction instruction) {
    switch (instruction) {
        case Instruction::ADD: case Instruction::SUB: return InstructionType::R;
        case Instruction::LDUR: case Instruction::STUR: return InstructionType::D;
        case Instruction::ADDI: case Instruction::SUBI: return InstructionType::I;
        case Instruction::B: return InstructionType::B;
        case Instruction::CBZ: case Instruction::CBNZ: return InstructionType::CB;
        default: throw std::invalid_argument("Unknown instruction");
    }
}

void Instr::print_verbose() {
    std::cout << "\n<<<<<<<<<<" << std::endl;
    
    switch (this->instr) {
        case Instruction::ADD: std::cout << "Instruction: 'ADD'" << std::endl; break;
        case Instruction::SUB: std::cout << "Instruction: 'SUB'" << std::endl; break;
        case Instruction::LDUR: std::cout << "Instruction: 'LDUR'" << std::endl; break;
        case Instruction::STUR: std::cout << "Instruction: 'STUR'" << std::endl; break;
        case Instruction::ADDI: std::cout << "Instruction: 'ADDI'" << std::endl; break;
        case Instruction::SUBI: std::cout << "Instruction: 'SUBI'" << std::endl; break;
        case Instruction::B: std::cout << "Instruction: 'B'" << std::endl; break;
        case Instruction::CBZ: std::cout << "Instruction: 'CBZ'" << std::endl; break;
        case Instruction::CBNZ: std::cout << "Instruction: 'CBNZ'" << std::endl; break;
    }

    switch (this->type) {
        case InstructionType::R: std::cout << "InstructionType 'R'" << std::endl; break;
        case InstructionType::D: std::cout << "InstructionType 'D'" << std::endl; break;
        case InstructionType::I: std::cout << "InstructionType 'I'" << std::endl; break;
        case InstructionType::B: std::cout << "InstructionType 'B'" << std::endl; break;
        case InstructionType::CB: std::cout << "InstructionType 'CB'" << std::endl; break;
    }

    for (auto arg: this->args) {
        std::cout << arg << " | ";
    }

    std::cout << std::endl << "&&&&&&&&&&&&&&&&&&&&&&&&&\n" << std::endl;
}

