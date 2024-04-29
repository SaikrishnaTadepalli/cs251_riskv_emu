import array

R_TYPE_INSTRUCTIONS = ["ADD", "SUB"]
D_TYPE_INSTRUCTIONS = ["LDUR", "STUR"]
I_TYPE_INSTRUCTIONS = ["ADDI", "SUBI"]
B_TYPE_INSTRUCTIONS = ["B"]
CB_TYPE_INSTRUCTIONS = ["CBZ", "CBNZ"]

MEMSIZE = 256

class CPU:
    def __init__(self, id, code):
        self.id = id
        self.pc = 0

        self.code = code

        self.registers = [0] * 32 # 64-bit integer array
        self.data_mem = [0] * MEMSIZE # 8-bit integer array

    def __str__(self):
        def pad_left(data, length): 
            data_str = str(data)
            if len(data_str) >= length: return data_str[:length]
            else: return ' ' * (length - len(data_str)) + data_str

        res = f"\nCPU ID: {self.id} ----------------------------------------\n\n"
        
        res += f"PC = {self.pc}\n\n"

        res += f"Registers:\n"
        for i in range(0, 16):
            res += f"\t{pad_left(f'X{i}', 4)}: {pad_left(self.registers[i], 20)}\t||\t{pad_left(f'X{i + 16}', 3)}: {pad_left(self.registers[i + 16], 20)}\n"

        res += "\nData Memory:\n"
        for i in range(0, MEMSIZE // 4, 4):
            c_w = MEMSIZE // 4
            c1, c2, c3, c4 = c_w * 0, c_w * 1, c_w * 2, c_w * 3

            res += f"\t{pad_left(c1 + i, 4)}: {pad_left(self.data_mem[c1 + i], 3)} {pad_left(self.data_mem[c1 + i + 1], 3)} {pad_left(self.data_mem[c1 + i + 2], 3)} {pad_left(self.data_mem[c1 + i + 3], 3)}"
            res += f"   ||  {pad_left(c2 + i, 4)}: {pad_left(self.data_mem[c2 + i], 3)} {pad_left(self.data_mem[c2 + i + 1], 3)} {pad_left(self.data_mem[c2 + i + 2], 3)} {pad_left(self.data_mem[c2 + i + 3], 3)}"
            res += f"   ||  {pad_left(c3 + i, 4)}: {pad_left(self.data_mem[c3 + i], 3)} {pad_left(self.data_mem[c3 + i + 1], 3)} {pad_left(self.data_mem[c3 + i + 2], 3)} {pad_left(self.data_mem[c3 + i + 3], 3)}"
            res += f"   ||  {pad_left(c4 + i, 4)}: {pad_left(self.data_mem[c4 + i], 3)} {pad_left(self.data_mem[c4 + i + 1], 3)} {pad_left(self.data_mem[c4 + i + 2], 3)} {pad_left(self.data_mem[c4 + i + 3], 3)}"
            res += "\n"
            
        res += "\n"
        
        return res

    def __print__(self):
        print(str(self))

    def __eq__(cpu1, cpu2):
        for R1, R2 in zip(cpu1.registers, cpu2.registers):
            if R1 != R2: return False
        
        for M1, M2 in zip(cpu1.data_mem, cpu2.data_mem):
            if M1 != M2: return False
        
        return True

    def write_state(self):
        state = str(self)

        f = open(f"{self.id} - state")
        f.write(state)
        f.close()

    def get_cur_instr(self):
        return self.code[self.pc // 4]
    
    def get_reg_index(reg: str) -> int:
        if reg == "XZR": return 31
        return int(reg[1:])

    def get_immediate(immediate: str) -> int:
        return int(immediate[1:])

    def next_instruction(self):
        def handle_r_type(instr, args):
            XA, XB, XC = args.split(",")

            XA = CPU.get_reg_index(XA)
            XB = CPU.get_reg_index(XB)
            XC = CPU.get_reg_index(XC)

            if instr == "ADD": new_val = self.registers[XB] + self.registers[XC]
            elif instr == "SUB": new_val = self.registers[XB] - self.registers[XC]

            self.set_register_val(XA, new_val)

            self.pc += 4
        
        def handle_d_type(instr, args):
            # Converts 'XA,[XB,#24]'-> 'XA,XB,#24'
            args = args.replace("[", "")
            args = args.replace("]", "")

            XA, XB, IMM = args.split(",")

            XA = CPU.get_reg_index(XA)
            XB = CPU.get_reg_index(XB)
            IMM = CPU.get_immediate(IMM)

            if instr == "LDUR":
                mem_index = self.registers[XB] + IMM

                value = 0
                for i in range(8):
                    value = value << 8
                    value += self.data_mem[mem_index + i]

                self.set_register_val(XA, value)
            elif instr == "STUR":
                mem_index = self.registers[XB] + IMM

                reg_val = self.registers[XA]
                for i in range(7, 0, -1):
                    cur_val = reg_val & 0xFF
                    reg_val >>= 8
                    self.set_mem_val(mem_index + i, cur_val)

            self.pc += 4
        
        def handle_i_type(instr, args):
            XA, XB, IMM = args.split(",")

            XA = CPU.get_reg_index(XA)
            XB = CPU.get_reg_index(XB)
            IMM = CPU.get_immediate(IMM)

            if instr == "ADDI": new_val = self.registers[XB] + IMM
            elif instr == "SUBI": new_val = self.registers[XB] - IMM

            self.set_register_val(XA, new_val)

            self.pc += 4
        
        def handle_b_type(instr, args):
            IMM = CPU.get_immediate(args)

            self.pc += 4 * IMM 
        
        def handle_cb_type(instr, args):
            XA, IMM = args.split(',')

            XA = CPU.get_reg_index(XA)
            IMM = CPU.get_immediate(IMM)

            step = IMM
            if instr == "CBZ" and self.registers[XA] != 0: step = 1
            elif instr == "CBNZ" and self.registers[XA] == 0: step = 1

            self.pc += 4 * step

        instr = (self.get_cur_instr()).split(' ')[0]
        args = ("".join((self.get_cur_instr()).split(' ')[1:])).replace(" ", "")

        # print(instr, " | ", args)

        if instr in R_TYPE_INSTRUCTIONS: handle_r_type(instr, args)
        elif instr in D_TYPE_INSTRUCTIONS: handle_d_type(instr, args)
        elif instr in I_TYPE_INSTRUCTIONS: handle_i_type(instr, args)
        elif instr in B_TYPE_INSTRUCTIONS: handle_b_type(instr, args)
        elif instr in CB_TYPE_INSTRUCTIONS: handle_cb_type(instr, args)
        else: 
            print("ERROR")
            self.pc = len(self.code) * 5

    def set_register_val(self, reg_index, value):
        self.registers[reg_index] = value

    def set_mem_val(self, mem_index, value):
        self.data_mem[mem_index] = value

    def run(self):
        while self.pc < len(self.code) * 4:
            self.next_instruction()

    def step(self):
        print(self)
        while self.pc < len(self.code) * 4:
            input()
            print(">>>>>", self.get_cur_instr())
            self.next_instruction()
            print(self)
    