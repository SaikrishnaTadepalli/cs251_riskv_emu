import random

import instr as Instr

# number of bytes in data memory
MEMSIZE = 256 

class CPU:
    def __init__(self, id, code):
        self.id = id
        self.pc = 0

        self.code = code

        self.registers = [0] * 32
        self.data_mem = [0] * MEMSIZE

    def __str__(self):
        def twos_complement_hex(number, num_bits):
            # Calculate the two's complement
            if number < 0: 
                number = (1 << num_bits) + number
            
            # Convert to hexadecimal
            hex_str = hex(number & ((1 << num_bits) - 1))
            
            # Pad with zeros if needed
            hex_str = hex_str[2:].zfill(num_bits // 4)
            hex_str = hex_str.upper()
            
            return ' '.join([hex_str[i:i+2] for i in range(0, len(hex_str), 2)])
        
        def pad_hex(num, length):
            return twos_complement_hex(num, length * 4)

        def pad_left(data, length, char=' '): 
            data_str = str(data)
            if len(data_str) >= length: return data_str[:length]
            else: return char * (length - len(data_str)) + data_str


        res = f"\nCPU ID: {self.id} {'-' * (65 - len(str(self.id)))}\n\n"
        
        res += f"PC = {self.pc}\n\n"

        res += f"Registers:\n"
        for i in range(0, 16):
            res += f"\t{pad_left(f'X{i}', 4)}: {pad_hex(self.registers[i], 16)}\t||   {pad_left(f'X{i + 16}', 3)}: {pad_hex(self.registers[i + 16], 16)}\n"
        
        res += "\nData Memory:\n"
        for i in range(0, MEMSIZE // 2, 8):
            c_w = MEMSIZE // 2
            c1, c2 = c_w * 0, c_w * 1

            d_hex = lambda x: pad_hex(self.data_mem[x], 2)

            res += f"\t{pad_left(c1 + i, 4)}: {d_hex(c1 + i + 0)} {d_hex(c1 + i + 1)} {d_hex(c1 + i + 2)} {d_hex(c1 + i + 3)} {d_hex(c1 + i + 4)} {d_hex(c1 + i + 5)} {d_hex(c1 + i + 6)} {d_hex(c1 + i + 7)}"
            res += f"   ||  {pad_left(c2 + i, 4)}: {d_hex(c2 + i + 0)} {d_hex(c2 + i + 1)} {d_hex(c2 + i + 2)} {d_hex(c2 + i + 3)} {d_hex(c2 + i + 4)} {d_hex(c2 + i + 5)} {d_hex(c2 + i + 6)} {d_hex(c2 + i + 7)}"
            res += "\n"

        res += f"\n{'-' * 74}\n\n"

        return res

    def __print__(self):
        print(str(self))

    def reg_eq(cpu1, cpu2):
        for R1, R2 in zip(cpu1.registers, cpu2.registers):
            if R1 != R2: return False
        return True
    
    def mem_eq(cpu1, cpu2):
        for M1, M2 in zip(cpu1.data_mem, cpu2.data_mem):
            if M1 != M2: return False
        return True

    def __eq__(cpu1, cpu2):
        return CPU.reg_eq(cpu1, cpu2) and CPU.mem_eq(cpu1, cpu2)

    def __ne__(cpu1, cpu2):
        return CPU.__eq__(cpu1, cpu2) == False

    def write_state(self, file_name):
        cpu_str = str(self)

        f = open(file_name)
        f.write(cpu_str)
        f.close()

    def get_cur_instr(self):
        i = (self.pc // 4)
        if i >= len(self.code):
            error_msg = f'''
            PC value out of bounds. 
            Expected PC < {len(self.code) * 4}. Recieved PC = {self.pc}.
            (Expected i < {len(self.code)}. Recieved i = {i}.)'
            '''
            raise IndexError(error_msg)
        return self.code[self.pc // 4].upper()

    def get_reg_index(reg):
        reg = reg.upper()

        error_msg = f'''
            Invalid register. Recieved '{reg}'.
        '''

        if reg == 'XZR': 
            return 31

        if len(reg) < 2: 
            raise ValueError(error_msg)
        
        try:
            reg_num = int(reg[1:])
        except ValueError:
            raise ValueError(error_msg)
    
        if reg_num < 0 or reg_num > 31: 
            raise ValueError(error_msg)

        return reg_num
    
    def get_immediate_value(imm):
        error_msg = f'''
            Invalid immediate value. Recieved '{imm}'.
        '''

        if len(imm) <= 1 or imm[0] != '#':
            raise ValueError(error_msg)
        
        try:
            imm_num = int(imm[1:])
        except ValueError:
            raise ValueError(error_msg)

        return imm_num
    
    def get_reg_value(self, reg: str):
        reg_index = CPU.get_reg_index(reg)
        return self.registers[reg_index]
    
    def set_reg_value(self, reg: str, value):
        reg_index = CPU.get_reg_index(reg)
        self.set_register_val(reg_index, value)
    
    def get_double_word(self, mem_index):
        res = 0
        for i in range(8):
            res <<= 8
            res += self.data_mem[mem_index + i]
        return res
    
    def set_double_word(self, mem_index, value):
        for i in range(7, -1, -1):
            temp = value & 0xFF
            value >>= 8
            self.set_mem_val(mem_index + i, temp)

    def set_register_val(self, reg_index: int, value: int):
        if reg_index < 0 or reg_index >= len(self.registers):
            error_msg = f'''
            Invalid Register Index. Recieved {reg_index}.
            '''
            raise IndexError(error_msg)
        
        self.registers[reg_index] = value

    def set_mem_val(self, mem_index: int, value: int):
        if mem_index < 0 or mem_index >= MEMSIZE:
            error_msg = f'''
            Invalid Memory Index. Recieved {mem_index}.
            '''
            raise IndexError(error_msg)
        
        self.data_mem[mem_index] = value

    def randomize_register(self, reg_index):
        rand_val = random.randrange(2 ** 64)
        self.set_register_val(reg_index, rand_val)

    def randomize_mem_byte(self, byte_index):
        rand_val = random.randrange(2 ** 8)
        self.set_mem_val(byte_index, rand_val)

    def randomize_registers(self):
        for i in range(len(self.registers) - 1):
            self.randomize_register(i)

    def randomize_data_memory(self):
        for i in range(len(self.data_mem)):
            self.randomize_mem_byte(i)

    def randomize_cpu(self):
        self.randomize_registers()
        self.randomize_data_memory()
    
    def run_instr(self):
        # Get current Instruction
        instr_values = Instr.Instr.extract(self.get_cur_instr())
        
        # Seperate Instruction and Instruction Args
        instr, args = instr_values.instr, instr_values.args

        def run_r_type():
            try:
                XA, XB, XC = args
            except:
                error_msg = f'''
                Invalid args.
                Recieved {args}.
                Expected type: ['XA', 'XB', 'XC'].
                '''
                raise ValueError(error_msg)

            XA = CPU.get_reg_index(XA)
            XB = CPU.get_reg_index(XB)
            XC = CPU.get_reg_index(XC)

            if instr == Instr.Instr.ADD:
                # Compute value to be put in XA
                new_val = self.registers[XB] + self.registers[XC]
            elif instr == Instr.Instr.SUB:
                # Compute value to be put in XA
                new_val = self.registers[XB] - self.registers[XC]
            else:
                error_msg = f'''
                Unknown R-type instruction. Recieved '{instr}'
                '''
                raise ValueError(error_msg)
            
            # Place new value in XA
            self.set_register_val(XA, new_val)
            
            # Increment PC to next instruction
            self.pc += 4

        def run_d_type():
            try:
                XA, XB, IMM = args
            except:
                error_msg = f'''
                Invalid args.
                Recieved {args}.
                Expected type: ['XA', 'XB', 'IMM'].
                '''
                raise ValueError(error_msg)

            XA = CPU.get_reg_index(XA)
            XB = CPU.get_reg_index(XB)
            IMM = CPU.get_immediate_value(IMM)

            #Enforcing IMM bounds
            if not (-256 <= IMM <= 255):
                error_msg = f'''
                Immediete Value invalid. 
                Recieved IMM = {IMM}.
                Expected -256 <= IMM <= 255.
                '''
                raise ValueError(error_msg)
            
            mem_index = self.registers[XB] + IMM

            # Memory Access must be double word aligned
            if (mem_index % 8 != 0):
                error_msg = f'''
                Memory Access invalid.
                Recieved access index = {mem_index}.
                Access Index must be double-word aligned.
                '''
                raise ValueError(error_msg)

            if instr == Instr.Instr.LDUR:
                mem_value = self.get_double_word(mem_index)
                self.set_register_val(XA, mem_value)
            elif instr == Instr.Instr.STUR:
                reg_val = self.registers[XA]
                self.set_double_word(mem_index, reg_val)
            else:
                error_msg = f'''
                Unknown D-type instruction. Recieved '{instr}'
                '''
                raise ValueError(error_msg)
            
            # Increment PC to next instruction
            self.pc += 4

        def run_i_type():
            try:
                XA, XB, IMM = args
            except:
                error_msg = f'''
                Invalid args.
                Recieved {args}.
                Expected type: ['XA', 'XB', 'IMM'].
                '''
                raise ValueError(error_msg)

            XA = CPU.get_reg_index(XA)
            XB = CPU.get_reg_index(XB)
            IMM = CPU.get_immediate_value(IMM)

            # Enforcing IMM bounds
            if not (0 <= IMM <= 4095):
                error_msg = f'''
                Immediete Value invalid. 
                Recieved IMM = {IMM}.
                Expected 0 <= IMM <= 4095.
                '''
                raise ValueError(error_msg)

            if instr == Instr.Instr.ADDI:
                # Compute value to be put in XA
                new_val = self.registers[XB] + IMM
            elif instr == Instr.Instr.SUBI:
                # Compute value to be put in XA
                new_val = self.registers[XB] - IMM
            else:
                error_msg = f'''
                Unknown I-type instruction. Recieved '{instr}'
                '''
                raise ValueError(error_msg)
            
            # Place new value in XA
            self.set_register_val(XA, new_val)
            
            # Increment PC to next instruction
            self.pc += 4

        def run_b_type():
            try:
                IMM = args
            except:
                error_msg = f'''
                Invalid args.
                Recieved {args}.
                Expected type: ['IMM'].
                '''
                raise ValueError(error_msg)
            
            IMM = CPU.get_immediate_value(IMM)

            # Enforcing IMM bounds
            if not (-33554432 <= IMM <= 33554431):
                error_msg = f'''
                Immediete Value invalid. 
                Recieved IMM = {IMM}.
                Expected -33 554 432 <= IMM <= 33 554 431.
                '''
                raise ValueError(error_msg)

            # Set new PC value
            self.pc += 4 * IMM

        def run_cb_type():
            try:
                XA, IMM = args
            except:
                error_msg = f'''
                Invalid args.
                Recieved {args}.
                Expected type: ['XA', 'IMM'].
                '''
                raise ValueError(error_msg)
            
            XA = CPU.get_reg_index(XA)
            IMM = CPU.get_immediate_value(IMM)

            # Enforcing IMM bounds
            if not (-262144 <= IMM <= 262143):
                error_msg = f'''
                Immediete Value invalid. 
                Recieved IMM = {IMM}.
                Expected -262 144 <= IMM <= 262 143.
                ''' 
                raise ValueError(error_msg)
            
            step = 1
            if instr == Instr.Instr.CBZ:
                if self.registers[XA] == 0: step = IMM
            elif instr == Instr.Instr.CBNZ:
                if self.registers[XA] != 0: step = IMM
            else:
                error_msg = f'''
                Unknown CB-type instruction. Recieved '{instr}'
                '''
                raise ValueError(error_msg)

            # Set new PC value
            self.pc += 4 * step

        if instr in Instr.Instr.R_TYPE: run_r_type()
        elif instr in Instr.Instr.D_TYPE: run_d_type()
        elif instr in Instr.Instr.I_TYPE: run_i_type()
        elif instr in Instr.Instr.B_TYPE: run_b_type()
        elif instr in Instr.Instr.CB_TYPE: run_cb_type()
        else:
            error_msg = f'''
            Invalid Instruction.
            Recieved '{self.get_cur_instr()}' where:
                - 'instr' is '{instr}'
                - 'args' is {args}
            '''
            raise ValueError(error_msg)

    def run(self):
        while self.pc < len(self.code) * 4:
            self.run_instr()
    
    def step(self):
        print(f"Executing {'=' * 64}\n")
        print("Initial State: ")
        print(self)
        while self.pc < len(self.code) * 4:
            input()
            print("Instructions:")
            for i, instr in enumerate(self.code):
                line = f"\t{f'{i * 4: >3}'}: " + f"{instr: <25}"
                if i == (self.pc // 4): line += "\t<<< Just Executed"
                print(line)
            self.run_instr()
            print(self)
        print(f"Finished {'=' * 65}")